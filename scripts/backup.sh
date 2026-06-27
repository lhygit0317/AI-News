#!/bin/bash
# xFusion 情报系统 Git 备份脚本
# 将技能和报告推送到 GitHub 备份仓库

set -e

BACKUP_DIR="$HOME/.hermes-backup"
SKILL_DIR="$HOME/.hermes/skills/xfusion-intelligence"
REPORT_DIR="$HOME/.hermes/workspace/intelligence-reports"
LOG_FILE="$BACKUP_DIR/backup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查备份目录
if [ ! -d "$BACKUP_DIR" ]; then
    log "[WARN] 备份目录不存在: $BACKUP_DIR"
    log "[INFO] 请先初始化备份仓库: git clone <backup-repo-url> $BACKUP_DIR"
    exit 0
fi

cd "$BACKUP_DIR"

# 同步技能文件
log "[INFO] 同步技能文件..."
if [ -d "$SKILL_DIR" ]; then
    mkdir -p assets/skills/xfusion-intelligence
    rsync -av --delete "$SKILL_DIR/" assets/skills/xfusion-intelligence/ 2>/dev/null || \
        cp -r "$SKILL_DIR/"* assets/skills/xfusion-intelligence/ 2>/dev/null
fi

# 同步报告
log "[INFO] 同步情报报告..."
if [ -d "$REPORT_DIR" ]; then
    mkdir -p assets/workspace/intelligence-reports
    rsync -av --delete "$REPORT_DIR/" assets/workspace/intelligence-reports/ 2>/dev/null || \
        cp -r "$REPORT_DIR/"* assets/workspace/intelligence-reports/ 2>/dev/null
fi

# Git 提交
if git status --porcelain | grep -q .; then
    log "[INFO] 检测到变更，准备提交..."
    git add -A
    git commit -m "backup: auto-backup $(date '+%Y-%m-%d %H:%M')"
    
    if git push origin main 2>&1 | tee -a "$LOG_FILE"; then
        log "[OK] Backup pushed to GitHub"
    else
        log "[ERROR] Git push 失败"
    fi
else
    log "[INFO] 无变更，跳过备份"
fi
