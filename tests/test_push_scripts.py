import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FeishuSummaryTests(unittest.TestCase):
    def test_extract_summary_uses_headings_not_inline_emoji(self):
        push_feishu = load_script_module("push_feishu", "scripts/push-feishu.py")
        report = """# 超聚变行业周报
**周期：2026-06-24 至 2026-07-01**

## 🔵 一、电源与液冷
- 🔴 电源供应链紧张，需要二供评估

## 🟢 二、AI大模型动态
1. **OpenAI** 发布企业模型更新

## 🟡 三、AI基础设施方案
- VMware 推进私有云 AI

## 🔴 四、太空算力
- AWS 发布卫星边缘计算合作

## ⚪ 五、人力资源
- 华为 AI 岗位扩招

## 📌 本周核心结论
1. 国产 AI 服务器需求继续上升
"""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md") as tmp:
            tmp.write(report)
            tmp.flush()

            summary = push_feishu.extract_summary_from_report(tmp.name, max_chars=800)

        self.assertIn("周期：2026-06-24 至 2026-07-01", summary)
        self.assertIn("🔵 电源/液冷：电源供应链紧张，需要二供评估", summary)
        self.assertIn("🟢 AI模型：OpenAI 发布企业模型更新", summary)
        self.assertIn("🟡 AI方案：VMware 推进私有云 AI", summary)
        self.assertIn("🔴 太空算力：AWS 发布卫星边缘计算合作", summary)
        self.assertIn("⚪ 人才：华为 AI 岗位扩招", summary)
        self.assertIn("📌 国产 AI 服务器需求继续上升", summary)

    def test_extract_summary_handles_existing_table_report(self):
        push_feishu = load_script_module("push_feishu", "scripts/push-feishu.py")

        summary = push_feishu.extract_summary_from_report(
            str(REPO_ROOT / "reports/2026-W26-xfusion-weekly.md"), max_chars=500
        )

        self.assertIn("🔵 电源/液冷：", summary)
        self.assertIn("🟢 AI模型：", summary)
        self.assertIn("🟡 AI方案：", summary)
        self.assertIn("🔴 太空算力：", summary)
        self.assertIn("⚪ 人才：", summary)
        self.assertNotIn("🔴 太空算力：液冷:", summary)
        self.assertNotIn("**", summary)

    def test_extract_summary_preserves_all_sections_under_default_limit(self):
        push_feishu = load_script_module("push_feishu", "scripts/push-feishu.py")

        summary = push_feishu.extract_summary_from_report(
            str(REPO_ROOT / "reports/2026-W26-xfusion-weekly.md")
        )

        self.assertLessEqual(len(summary), 200)
        self.assertIn("🔵 电源/液冷：", summary)
        self.assertIn("🟢 AI模型：", summary)
        self.assertIn("🟡 AI方案：", summary)
        self.assertIn("🔴 太空算力：", summary)
        self.assertIn("⚪ 人才：", summary)


class EmailTemplateTests(unittest.TestCase):
    def test_email_template_inserts_dynamic_report_body(self):
        push_email = load_script_module("push_email", "scripts/push-email.py")

        html = push_email.load_email_template(
            "<h2>动态报告正文</h2>",
            "2026-06-24 - 2026-07-01",
            "dynamic-report.md",
        )

        self.assertIn("动态报告正文", html)
        self.assertIn("2026-06-24 - 2026-07-01", html)
        self.assertIn("dynamic-report.md", html)
        self.assertNotIn("2026年6月20日 - 6月27日", html)

    def test_email_cli_uses_smtp_port_from_environment(self):
        push_email = load_script_module("push_email", "scripts/push-email.py")
        captured = {}

        def fake_send_email(smtp_host, smtp_port, smtp_user, smtp_pass,
                            from_addr, to_addr, subject, html_body):
            captured["smtp_port"] = smtp_port
            return True

        env = {
            **os.environ,
            "SMTP_HOST": "smtp.163.com",
            "SMTP_PORT": "465",
            "SMTP_USER": "sender@example.com",
            "SMTP_PASS": "secret",
            "EMAIL_FROM": "sender@example.com",
            "EMAIL_TO": "receiver@example.com",
        }
        argv = [
            "push-email.py",
            "--report",
            str(REPO_ROOT / "reports/2026-W26-xfusion-weekly.md"),
            "--subject",
            "端口测试",
        ]

        with patch.dict(os.environ, env, clear=True), \
                patch.object(sys, "argv", argv), \
                patch.object(push_email, "send_email", fake_send_email), \
                self.assertRaises(SystemExit) as cm:
            push_email.main()

        self.assertEqual(cm.exception.code, 0)
        self.assertEqual(captured["smtp_port"], 465)


class DryRunCliTests(unittest.TestCase):
    def test_feishu_dry_run_does_not_require_webhook(self):
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts/push-feishu.py"),
                "--text",
                "测试消息",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            env={**os.environ, "FEISHU_WEBHOOK_URL": ""},
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("[DRY-RUN]", result.stdout)
        self.assertIn("测试消息", result.stdout)

    def test_email_dry_run_does_not_require_smtp(self):
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "scripts/push-email.py"),
                "--report",
                str(REPO_ROOT / "reports/2026-W26-xfusion-weekly.md"),
                "--subject",
                "测试邮件",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            env={
                key: value
                for key, value in os.environ.items()
                if key not in {"SMTP_HOST", "SMTP_USER", "SMTP_PASS", "EMAIL_TO"}
            },
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("[DRY-RUN]", result.stdout)
        self.assertIn("测试邮件", result.stdout)


class SkillMetadataTests(unittest.TestCase):
    def test_space_computing_deep_skill_has_correct_identity(self):
        skill_text = (REPO_ROOT / "skill/sub-skills/space-computing-deep/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("name: space-computing-deep", skill_text)
        self.assertIn("太空算力", skill_text)
        self.assertIn("LEO卫星", skill_text)
        self.assertNotIn("name: ai-software-deep", skill_text)


class DocumentationConsistencyTests(unittest.TestCase):
    def test_weekly_schedule_is_consistently_friday_only(self):
        checked_files = [
            REPO_ROOT / "docs/GETTING-STARTED.md",
            REPO_ROOT / "docs/OPERATIONS.md",
            REPO_ROOT / "skill/SKILL.md",
        ]

        for path in checked_files:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("schedule='0 9 * * 1'", text, path)
            self.assertNotIn("0 9 * * 3,5", text, path)
            self.assertNotIn("每周一 9:00", text, path)
            self.assertNotIn("每周一早上9点", text, path)
            self.assertNotIn("每周三/周五", text, path)
            self.assertNotIn("每周三和每周五", text, path)

        combined = "\n".join(path.read_text(encoding="utf-8") for path in checked_files)
        self.assertIn("0 9 * * 5", combined)


if __name__ == "__main__":
    unittest.main()
