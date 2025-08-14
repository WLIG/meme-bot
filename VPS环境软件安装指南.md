# VPS环境软件安装指南

## 概述

本指南旨在为用户提供在VPS（虚拟私人服务器）环境中安装和配置以下核心软件的详细步骤和一键式脚本：

*   **Python 3.8+**: 一种广泛使用的高级编程语言，适用于Web开发、数据分析、人工智能等。
*   **Node.js 18+**: 一个基于Chrome V8 JavaScript引擎的JavaScript运行时环境，用于构建高性能的网络应用。
*   **SQLite 3.x 或 PostgreSQL 13+**: 两种流行的关系型数据库管理系统。SQLite适用于轻量级应用或本地存储，而PostgreSQL则是一个功能强大、可扩展的企业级数据库。
*   **Nginx 1.20+**: 一个高性能的HTTP和反向代理服务器，也可作为邮件代理服务器和通用TCP/UDP代理服务器。

本指南将涵盖手动安装的详细步骤，并提供一个自动化安装的一键脚本，以简化部署过程。




## 1. Python 3.8+ 安装

Python是一种多用途的编程语言，广泛应用于Web开发、数据科学、机器学习等领域。为了确保兼容性和获取最新功能，建议安装Python 3.8或更高版本。在大多数Linux发行版中，Python 3通常已经预装，但版本可能不符合要求。本节将介绍如何通过系统包管理器或源代码编译的方式安装或升级Python。

### 1.1 使用系统包管理器安装 (推荐)

对于大多数VPS用户，使用系统自带的包管理器是安装Python最便捷和推荐的方式。以下是针对不同Linux发行版的安装命令。

#### Ubuntu/Debian

在Ubuntu和Debian系统中，可以使用`apt`命令来安装Python及其开发工具。首先，更新包列表以确保获取最新的软件包信息：

```bash
sudo apt update
```

然后，安装Python 3.8或更高版本。如果系统默认仓库中没有您需要的特定版本，可能需要添加PPA（Personal Package Archive）。例如，要安装Python 3.8：

```bash
sudo apt install python3.8 python3.8-venv python3.8-dev
```

`python3.8-venv`用于创建虚拟环境，这对于项目依赖管理至关重要。`python3.8-dev`包含开发所需的头文件和静态库，如果您计划编译Python扩展或安装某些需要编译的Python包，则需要它。

#### CentOS/RHEL

在CentOS和RHEL系统中，可以使用`yum`或`dnf`（CentOS 8+）命令来安装Python。首先，确保系统已安装EPEL（Extra Packages for Enterprise Linux）仓库，因为它提供了许多额外的软件包，包括较新版本的Python。

```bash
sudo yum install epel-release
sudo yum update
```

或者对于CentOS 8/RHEL 8及更高版本：

```bash
sudo dnf install epel-release
sudo dnf update
```

然后，安装Python 3.8或更高版本。CentOS/RHEL 8默认提供Python 3.8。您可以使用以下命令安装：

```bash
sudo dnf install python38 python38-devel
```

`python38-devel`类似于Ubuntu的`python3.8-dev`，提供开发所需的头文件和库。

### 1.2 验证Python安装

安装完成后，可以通过运行以下命令来验证Python版本：

```bash
python3.8 --version
```

或者，如果您的系统将Python 3.8设置为默认的`python3`命令：

```bash
python3 --version
```

您还应该验证`pip`（Python包安装器）是否可用，它通常随Python一起安装：

```bash
pip3 --version
```

如果`pip3`不可用，您可能需要单独安装它：

```bash
sudo apt install python3-pip # Ubuntu/Debian
sudo dnf install python3-pip # CentOS/RHEL
```

### 1.3 最佳实践：使用虚拟环境

强烈建议为每个Python项目使用虚拟环境。虚拟环境允许您在隔离的环境中安装项目依赖，避免不同项目之间的依赖冲突。以下是创建和激活虚拟环境的基本步骤：

```bash
python3.8 -m venv myproject_env
source myproject_env/bin/activate
```

激活虚拟环境后，您安装的任何Python包都将仅限于该环境。要退出虚拟环境，只需运行：

```bash
deactivate
```

通过遵循这些步骤，您可以在VPS上成功安装和配置Python 3.8+环境，为后续的开发工作奠定基础。




## 2. Node.js 18+ 安装

Node.js 是一个基于 Chrome V8 引擎的 JavaScript 运行时，用于构建可伸缩的网络应用。安装 Node.js 通常也包括 npm（Node Package Manager），它是 Node.js 的包管理器。建议安装 Node.js 18 或更高版本，因为这些版本通常是 LTS（长期支持）版本，提供更好的稳定性和支持。

### 2.1 使用包管理器安装 (推荐)

从官方 Node.js 仓库安装是获取最新稳定版本并确保未来更新的推荐方法。这比直接使用系统默认仓库中的旧版本更可靠。

#### Ubuntu/Debian

在 Ubuntu 和 Debian 系统上，您可以使用 `curl` 命令从 NodeSource 仓库添加 Node.js 的官方 APT 仓库。NodeSource 提供了最新的 Node.js 版本，并且易于安装和更新。

首先，确保您的系统已安装 `curl` 和 `gnupg`：

```bash
sudo apt update
sudo apt install -y curl gnupg
```

然后，添加 Node.js 18.x 的 NodeSource 仓库。请注意，`setup_18.x` 会根据您需要的版本进行更改（例如，如果您需要 Node.js 20.x，则使用 `setup_20.x`）。

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
```

执行上述命令后，NodeSource 仓库将被添加到您的系统，并且 APT 包列表会自动更新。现在，您可以安装 Node.js 和 npm：

```bash
sudo apt install -y nodejs
```

#### CentOS/RHEL

在 CentOS 和 RHEL 系统上，您同样可以使用 `curl` 命令从 NodeSource 仓库添加 Node.js 的官方 YUM/DNF 仓库。这确保您可以安装最新版本的 Node.js。

首先，确保您的系统已安装 `curl`：

```bash
sudo yum install -y curl # 或者 sudo dnf install -y curl
```

然后，添加 Node.js 18.x 的 NodeSource 仓库。同样，`setup_18.x` 可以根据需要更改为其他版本。

```bash
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo -E bash -
```

执行上述命令后，NodeSource 仓库将被添加到您的系统，并且 YUM/DNF 缓存会自动更新。现在，您可以安装 Node.js 和 npm：

```bash
sudo yum install -y nodejs # 或者 sudo dnf install -y nodejs
```

### 2.2 验证 Node.js 和 npm 安装

安装完成后，您可以通过运行以下命令来验证 Node.js 和 npm 的版本：

```bash
node -v
npm -v
```

您应该看到类似 `v18.x.x` 和 `9.x.x` 的版本号。这表明 Node.js 和 npm 已成功安装并可供使用。

### 2.3 推荐：使用 nvm (Node Version Manager)

对于需要管理多个 Node.js 版本的开发者来说，使用 nvm（Node Version Manager）是一个非常灵活和强大的工具。nvm 允许您轻松地安装、切换和管理不同版本的 Node.js，而无需 `sudo` 权限。

安装 nvm 的方法是运行其官方安装脚本：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```

安装完成后，您可能需要关闭并重新打开终端，或者运行 `source ~/.bashrc` (或 `~/.zshrc` 等，取决于您的 shell 配置) 来加载 nvm。然后，您可以使用 nvm 安装 Node.js 18.x：

```bash
nvm install 18
nvm use 18
nvm alias default 18
```

`nvm install 18` 会安装最新版本的 Node.js 18。`nvm use 18` 会将当前 shell 会话的 Node.js 版本设置为 18。`nvm alias default 18` 会将 Node.js 18 设置为默认版本，这样每次打开新终端时都会自动使用它。

使用 nvm，您可以轻松切换版本：

```bash
nvm use 20 # 切换到 Node.js 20
nvm use 18 # 切换回 Node.js 18
```

通过以上步骤，您可以根据自己的需求选择最适合的 Node.js 安装方法，并确保您的VPS环境已准备好进行Node.js开发。




## 3. 数据库安装：SQLite 3.x 或 PostgreSQL 13+

在您的VPS上，您可以选择安装轻量级的SQLite数据库，或者功能更强大的PostgreSQL数据库，具体取决于您的项目需求。

### 3.1 SQLite 3.x 安装

SQLite 是一个零配置、无服务器、自包含的事务性 SQL 数据库引擎。它非常适合小型应用、本地开发或作为嵌入式数据库使用。大多数 Linux 发行版都预装了 SQLite，但您可能需要安装开发库以便与其他编程语言（如 Python）进行交互。

#### Ubuntu/Debian

在 Ubuntu 和 Debian 系统上，安装 SQLite 3 及其开发库非常简单：

```bash
sudo apt update
sudo apt install -y sqlite3 libsqlite3-dev
```

`sqlite3` 是 SQLite 命令行工具，`libsqlite3-dev` 提供了开发所需的头文件和库。

#### CentOS/RHEL

在 CentOS 和 RHEL 系统上，安装 SQLite 3 及其开发库：

```bash
sudo yum install -y sqlite sqlite-devel # 或者 sudo dnf install -y sqlite sqlite-devel
```

`sqlite` 是 SQLite 命令行工具，`sqlite-devel` 提供了开发所需的头文件和库。

#### 验证 SQLite 安装

安装完成后，您可以通过运行以下命令来验证 SQLite 版本：

```bash
sqlite3 --version
```

您应该看到类似 `3.x.x` 的版本号。

### 3.2 PostgreSQL 13+ 安装

PostgreSQL 是一个功能强大、开源的对象关系型数据库系统，以其可靠性、功能健壮性和高性能而闻名。它适用于需要高并发、复杂查询和大量数据的企业级应用。

#### Ubuntu/Debian

在 Ubuntu 和 Debian 系统上，安装 PostgreSQL 的推荐方法是使用官方 PostgreSQL APT 仓库，以确保您能获取到最新版本。

首先，导入 PostgreSQL 签名密钥：

```bash
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
```

然后，添加 PostgreSQL 仓库。请将 `$(lsb_release -cs)` 替换为您的 Ubuntu/Debian 版本代号（例如 `jammy` 对于 Ubuntu 22.04，`bullseye` 对于 Debian 11）。

```bash
echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
```

更新包列表并安装 PostgreSQL 13 或更高版本（例如，安装 PostgreSQL 16）：

```bash
sudo apt update
sudo apt install -y postgresql-16
```

这将安装 PostgreSQL 服务器、客户端工具以及其他必要的组件。

#### CentOS/RHEL

在 CentOS 和 RHEL 系统上，安装 PostgreSQL 的推荐方法是使用 PostgreSQL YUM 仓库。

首先，安装 PostgreSQL 仓库 RPM：

```bash
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm # 对于 RHEL/CentOS 8
# 或者 sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm # 对于 RHEL/CentOS 7
```

然后，禁用内置的 PostgreSQL 模块（如果存在）并安装 PostgreSQL 13 或更高版本（例如，安装 PostgreSQL 16）：

```bash
sudo dnf -qy module disable postgresql # 对于 RHEL/CentOS 8
sudo dnf install -y postgresql16-server postgresql16-contrib
```

初始化数据库并启动 PostgreSQL 服务：

```bash
sudo /usr/pgsql-16/bin/postgresql-16-setup initdb
sudo systemctl enable postgresql-16
sudo systemctl start postgresql-16
```

#### 配置 PostgreSQL

安装 PostgreSQL 后，您需要进行一些基本配置。默认情况下，PostgreSQL 会创建一个名为 `postgres` 的数据库用户，该用户具有超级用户权限。

切换到 `postgres` 用户并进入 PostgreSQL 命令行：

```bash
sudo -i -u postgres
psql
```

在 `psql` 提示符下，您可以设置 `postgres` 用户的密码，并创建新的数据库和用户：

```sql
ALTER USER postgres WITH PASSWORD 'your_strong_password';
CREATE DATABASE mydatabase;
CREATE USER myuser WITH PASSWORD 'another_strong_password';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
\q
```

退出 `postgres` 用户：

```bash
exit
```

#### 验证 PostgreSQL 安装

您可以通过尝试连接到数据库来验证 PostgreSQL 是否正在运行：

```bash
psql -h localhost -U myuser -d mydatabase
```

输入您为 `myuser` 设置的密码。如果成功连接，您将进入 `psql` 命令行界面，表示 PostgreSQL 已成功安装和配置。输入 `\q` 退出。




## 4. Nginx 1.20+ 安装

Nginx（发音为 “engine-x”）是一个高性能的HTTP和反向代理服务器，也可以用作邮件代理服务器和通用TCP/UDP代理服务器。它以其高性能、稳定性、丰富的功能集和低资源消耗而闻名。建议安装 Nginx 1.20 或更高版本。

### 4.1 使用包管理器安装 (推荐)

从官方仓库安装 Nginx 是最直接和推荐的方式，可以确保您获得稳定且经过测试的版本。

#### Ubuntu/Debian

在 Ubuntu 和 Debian 系统上，Nginx 可以在默认的 APT 仓库中找到。首先，更新包列表：

```bash
sudo apt update
```

然后，安装 Nginx：

```bash
sudo apt install -y nginx
```

安装完成后，Nginx 服务通常会自动启动。您可以使用以下命令检查其状态：

```bash
sudo systemctl status nginx
```

如果 Nginx 没有运行，您可以使用以下命令启动它：

```bash
sudo systemctl start nginx
```

并使其在系统启动时自动运行：

```bash
sudo systemctl enable nginx
```

#### CentOS/RHEL

在 CentOS 和 RHEL 系统上，Nginx 也可以通过 `yum` 或 `dnf` 包管理器安装。首先，您可能需要启用 EPEL 仓库，因为 Nginx 通常在该仓库中提供。

```bash
sudo yum install -y epel-release # 或者 sudo dnf install -y epel-release
```

然后，安装 Nginx：

```bash
sudo yum install -y nginx # 或者 sudo dnf install -y nginx
```

安装完成后，启动 Nginx 服务并使其在系统启动时自动运行：

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

您可以使用以下命令检查其状态：

```bash
sudo systemctl status nginx
```

### 4.2 配置防火墙

如果您的 VPS 上启用了防火墙（例如 `ufw` 或 `firewalld`），您需要允许 HTTP (80) 和 HTTPS (443) 流量通过，以便外部用户可以访问您的 Nginx 服务器。

#### Ubuntu/Debian (UFW)

```bash
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
sudo ufw reload
```

#### CentOS/RHEL (firewalld)

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 4.3 验证 Nginx 安装

安装并启动 Nginx 后，您可以通过在 Web 浏览器中访问您的 VPS 的公共 IP 地址或域名来验证 Nginx 是否正常工作。如果一切正常，您应该会看到 Nginx 的默认欢迎页面。

您也可以使用 `curl` 命令在服务器内部进行验证：

```bash
curl http://localhost
```

这将返回 Nginx 默认页面的 HTML 内容。

### 4.4 Nginx 常用命令

以下是一些常用的 Nginx 服务管理命令：

*   **启动 Nginx**: `sudo systemctl start nginx`
*   **停止 Nginx**: `sudo systemctl stop nginx`
*   **重启 Nginx**: `sudo systemctl restart nginx`
*   **重新加载 Nginx 配置**: `sudo systemctl reload nginx` (在不中断服务的情况下应用配置更改)
*   **检查 Nginx 配置语法**: `sudo nginx -t`
*   **查看 Nginx 服务状态**: `sudo systemctl status nginx`

通过这些步骤，您可以在 VPS 上成功安装和配置 Nginx，并为您的 Web 应用程序提供高性能的反向代理和静态文件服务。




## 5. 一键安装脚本使用说明

为了简化安装过程，我们提供了一个一键安装脚本。该脚本会自动检测您的操作系统类型（Ubuntu/Debian 或 CentOS/RHEL），并尝试安装所需的所有软件。

### 5.1 脚本下载与执行

1.  **下载脚本**：

    您可以通过以下命令将脚本下载到您的VPS上：

    ```bash
wget https://raw.githubusercontent.com/your_repo/your_script_name.sh -O install_vps_software.sh
    ```

    *注意：请将 `https://raw.githubusercontent.com/your_repo/your_script_name.sh` 替换为脚本的实际下载链接。目前脚本保存在本地，您需要手动上传到您的VPS。*

2.  **添加执行权限**：

    ```bash
chmod +x install_vps_software.sh
    ```

3.  **运行脚本**：

    ```bash
sudo ./install_vps_software.sh
    ```

    脚本执行过程中，会询问您是否安装 PostgreSQL。如果您选择 `n`，则会安装 SQLite。

### 5.2 脚本功能概述

*   **操作系统检测**：自动识别 Ubuntu/Debian 或 CentOS/RHEL 系统。
*   **Python 安装**：安装 Python 3.8+，并设置 `python3` 和 `pip3` 命令指向新安装的版本。
*   **Node.js 安装**：通过 NodeSource 官方仓库安装 Node.js 18+。
*   **数据库选择**：提供安装 SQLite 3.x 或 PostgreSQL 13+ 的选项。
*   **Nginx 安装**：安装 Nginx 1.20+，并启动服务。

### 5.3 注意事项

*   **防火墙配置**：脚本不会自动配置防火墙规则。安装 Nginx 后，请务必根据您的防火墙类型（UFW 或 firewalld）手动开放 HTTP (80) 和 HTTPS (443) 端口，如本指南第 4.2 节所述。
*   **PostgreSQL 配置**：如果选择安装 PostgreSQL，脚本只会安装数据库服务。您需要手动切换到 `postgres` 用户并使用 `psql` 命令来设置数据库用户密码、创建数据库和用户，如本指南第 3.2 节所述。
*   **Python 虚拟环境**：强烈建议在您的 Python 项目中使用虚拟环境，以避免依赖冲突。脚本安装 Python 后，您可以按照本指南第 1.3 节的说明创建和使用虚拟环境。
*   **Node.js 版本管理**：如果需要管理多个 Node.js 版本，建议在脚本安装 Node.js 后，手动安装 `nvm` 并使用它来管理 Node.js 版本，如本指南第 2.3 节所述。
*   **Nginx 版本**：在某些操作系统版本中，系统默认仓库提供的 Nginx 版本可能略低于 1.20+，但通常也足够满足大部分需求。脚本会尝试安装最新可用版本。

## 6. 总结

本指南提供了在VPS环境中安装 Python 3.8+、Node.js 18+、SQLite 3.x/PostgreSQL 13+ 和 Nginx 1.20+ 的详细步骤和一键安装脚本。通过遵循这些说明，您可以快速搭建起一个功能完善的开发或生产环境。请务必注意防火墙和数据库的额外配置步骤，以确保您的系统安全和正常运行。

---

