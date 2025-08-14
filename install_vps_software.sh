#!/bin/bash

# VPS环境软件一键安装脚本
# 支持 Ubuntu/Debian 和 CentOS/RHEL 系统

# 检查是否以root用户运行
if [ "$EUID" -ne 0 ]; then
    echo "请以root用户或使用sudo运行此脚本。"
    exit 1
fi

# 自动检测操作系统类型
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION_ID=$VERSION_ID
else
    echo "无法检测操作系统类型。"
    exit 1
fi

echo "检测到操作系统: $OS $VERSION_ID"

# 函数：安装Python 3.8+
install_python() {
    echo "\n--- 正在安装 Python 3.8+ ---"
    if command -v python3.8 &>/dev/null; then
        echo "Python 3.8+ 已安装。"
    else
        if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
            apt update
            apt install -y python3.8 python3.8-venv python3.8-dev python3-pip
            update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
        elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
            dnf install -y epel-release
            dnf update -y
            dnf install -y python38 python38-devel python3-pip
            update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
        else
            echo "不支持的操作系统，请手动安装 Python 3.8+。"
            return 1
        fi
        echo "Python 3.8+ 安装完成。"
    fi
    python3 --version
    pip3 --version
}

# 函数：安装Node.js 18+
install_nodejs() {
    echo "\n--- 正在安装 Node.js 18+ ---"
    if command -v node &>/dev/null && node -v | grep -q "v18\|v19\|v20\|v21\|v22\|v23\|v24\|v25\|v26\|v27\|v28\|v29"; then
        echo "Node.js 18+ 已安装。"
    else
        if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
            apt update
            apt install -y curl gnupg
            curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
            apt install -y nodejs
        elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
            dnf install -y curl
            curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
            dnf install -y nodejs
        else
            echo "不支持的操作系统，请手动安装 Node.js 18+。"
            return 1
        fi
        echo "Node.js 18+ 安装完成。"
    fi
    node -v
    npm -v
}

# 函数：安装SQLite 3.x
install_sqlite() {
    echo "\n--- 正在安装 SQLite 3.x ---"
    if command -v sqlite3 &>/dev/null && sqlite3 --version | grep -q "^3"; then
        echo "SQLite 3.x 已安装。"
    else
        if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
            apt update
            apt install -y sqlite3 libsqlite3-dev
        elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
            dnf install -y sqlite sqlite-devel
        else
            echo "不支持的操作系统，请手动安装 SQLite 3.x。"
            return 1
        fi
        echo "SQLite 3.x 安装完成。"
    fi
    sqlite3 --version
}

# 函数：安装PostgreSQL 13+
install_postgresql() {
    echo "\n--- 正在安装 PostgreSQL 13+ ---"
    if command -v psql &>/dev/null && psql --version | grep -q "(PostgreSQL) 1[3-9]\|2[0-9]"; then
        echo "PostgreSQL 13+ 已安装。"
    else
        if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
            curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
            echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
            apt update
            apt install -y postgresql-16 # 安装最新稳定版，目前为16
        elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
            dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(echo $VERSION_ID | cut -d'.' -f1)-x86_64/pgdg-redhat-repo-latest.noarch.rpm
            dnf -qy module disable postgresql
            dnf install -y postgresql16-server postgresql16-contrib
            /usr/pgsql-16/bin/postgresql-16-setup initdb
            systemctl enable postgresql-16
            systemctl start postgresql-16
        else
            echo "不支持的操作系统，请手动安装 PostgreSQL 13+。"
            return 1
        fi
        echo "PostgreSQL 13+ 安装完成。"
        echo "请手动配置PostgreSQL用户和数据库：sudo -i -u postgres psql"
    fi
    systemctl status postgresql || true
}

# 函数：安装Nginx 1.20+
install_nginx() {
    echo "\n--- 正在安装 Nginx 1.20+ ---"
    if command -v nginx &>/dev/null && nginx -v 2>&1 | grep -q "nginx/1\.\(2[0-9]\|[3-9][0-9]\)\|nginx/[2-9][0-9]"; then
        echo "Nginx 1.20+ 已安装。"
    else
        if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
            apt update
            apt install -y nginx
        elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
            dnf install -y epel-release
            dnf install -y nginx
        else
            echo "不支持的操作系统，请手动安装 Nginx 1.20+。"
            return 1
        fi
        echo "Nginx 1.20+ 安装完成。"
        systemctl enable nginx
        systemctl start nginx
        echo "请配置防火墙以允许HTTP/HTTPS流量。"
    fi
    nginx -v
    systemctl status nginx || true
}

# 主安装流程

# 询问用户是否安装PostgreSQL，否则安装SQLite
read -p "您想安装 PostgreSQL (y/n)? (如果选择n，将安装SQLite) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    INSTALL_POSTGRES=true
else
    INSTALL_POSTGRES=false
fi

install_python
install_nodejs

if [ "$INSTALL_POSTGRES" = true ]; then
    install_postgresql
else
    install_sqlite
fi

install_nginx

echo "\n--- 所有请求的软件安装完成！---"
echo "请根据需要手动配置防火墙和PostgreSQL用户。"


