
# Project S.L.I.C.E

![License](https://img.shields.io/badge/license-MIT-blue.svg)

![Version](https://img.shields.io/badge/version-0.1.0-brightgreen.svg)
  
S.L.I.C.E. (System for Leadership, Interaction, and Community Engagement) is an open-source tool designed to simplify and optimize Web3 community management. It integrates essential features such as security, gacha box mechanics, governance integrations, wallet checkers, and off-chain economic models into a single, comprehensive platform.

---

## 📋 Table of Contents

1. [About the Project](#-about-the-project)  
2. [Pre-requisites](#-pre-requisites)  
3. [Installation](#-installation)  
4. [Usage](#-usage)  
5. [Features](#-features)
6. [Contributing](#-contributing)  
7. [License](#-license)  
8. [Contact](#-contact)

---

## 📖 About the Project

Web3 communities shouldn’t have to rely on expensive, fragmented tools to stay secure, engaged, and growing. Right now, projects juggle multiple paid bots, each competing for attention, diluting their own brand in the process.

S.L.I.C.E. changes that. It’s an open-source, all-in-one platform that unifies security, engagement, and governance under one roof. No more clutter, no more extra costs, just a streamlined system that keeps your community strong and your brand front and center.

We built S.L.I.C.E. to give Web3 projects control over their own spaces while fostering a healthier, more connected ecosystem. It’s time to take back ownership and build the future of Web3, one community at a time.



### Built With

This project was built using the following tools and technologies:

  

#### 🐍 **Python Ecosystem**

- **[Python](https://www.python.org/):** The primary programming language for this project, known for its simplicity and versatility.

- **[Discord.py](https://discordpy.readthedocs.io/):** A Python library for interacting with the Discord API, used to build bots and other Discord-based integrations.

  

#### 🧰 **Code Quality and Formatting**

- **[Black](https://black.readthedocs.io/):** An opinionated code formatter for Python that enforces consistent styling automatically.

- **[Flake8](https://flake8.pycqa.org/):** A static analysis tool for Python that ensures adherence to code quality and style guidelines by combining pyflakes, pycodestyle, and McCabe.

- **[Bandit](https://bandit.readthedocs.io/):** A security analysis tool for Python that scans for common vulnerabilities in the codebase.

  

#### 🧪 **Testing and Coverage**

- **[Pytest](https://docs.pytest.org/):** A robust testing framework for Python that supports unit, functional, and integration tests.

- **[Coverage](https://coverage.readthedocs.io/):** Measures test coverage, providing insights into which parts of the code are not adequately tested.

  

#### 📦 **Dependency Management**

- **[Poetry](https://python-poetry.org/):** A modern tool for dependency management and packaging in Python, simplifying the installation and maintenance of project dependencies.

  

#### 🔄 **Automation and Continuous Integration**


- **[GitHub Actions](https://github.com/features/actions):** Automates workflows such as building, testing, and deploying code with custom workflows written in YAML.

- Example configuration located in `.github/workflows/ci.yaml`.

- **[Codecov](https://about.codecov.io/):** Collects and visualizes test coverage data to ensure high-quality code and provides reports integrated with GitHub.

  

#### 💬 **Communication**

- **[Discord](https://discord.gg/pXaZdHpS5b):** Used as a primary communication and integration platform for bots and other interactive components.

---

## 🛠️ Pre-requisites

Before installing, ensure you have the following installed:

- **Python 3.9+**
- **Poetry** for dependency management (`curl -sSL https://install.python-poetry.org | python3 -`)
- **PostgreSQL 13+** (running)

To install PostgreSQL:

- **Linux (Debian/Ubuntu):**  
  ```bash
  sudo apt update && sudo apt install postgresql postgresql-contrib
  sudo systemctl start postgresql  
   ```
- **macOS(Homebrew):**
  ```bash
  brew install postgresql
  brew services start postgresql
  ```   
- **Windows:** Download and install from [PostgreSQL Official Site](https://www.postgresql.org/download/)

## ⚙️ Installation

Provide a step-by-step guide for installation:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```
   
2. **Install Poetry**  
    If you haven’t installed Poetry yet, run:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    Then, configure Poetry to use your Python version (if necessary):
    ```bash
    poetry env use python3.12  # Replace with your Python version
    ```
   
3. **Install Dependencies**  
    With Poetry installed, install all required dependencies:
    ```bash
    poetry install
    ```
   
4. **Configure Environment Variables**  
    Before running the project, create a `.env file` based on the provided `.env.example`:
    ```bash
    cp .env.example .env
    ```
    Then, edit `.env` and fill in the required values:

    - Database credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`)
    - API keys
    - Bot tokens 

5. **Set Up the Database (PostgreSQL)**  
    Ensure PostgreSQL is installed and running, then create the database:
    ```bash
    createdb slice_db
    ```
    Note: The database credentials should match those in your `.env` file.

6. **Initialize Aerich (Database Migrations)**  
    Run the following commands to initialize and prepare the database migrations:
    ```bash
    poetry run aerich init-db
    ```
## 🚀 Usage

Once everything is set up, you can start the bot with:

```bash
poetry run python -m src.main
```
---

### ✨ Features

Highlight the key features of the project:

✅ **Captcha Verification (Moderation):** Verification system for new members to prevent bots and fake accounts.

🔔 **NFT Sales Notifications (Automation):** Notifies the server about NFT sales on OpenSea, including details like price, buyer, seller, and image.

🔐 **Holder Verification (Engagement):** New members verify ownership of an NFT by signing a wallet message. Upon successful verification, they receive the "Holder" role, granting full access to the token-gated server.

🎁 **Mystery-Box System (Gamification):** Users can open mystery boxes and receive random rewards, enhancing engagement and activity.

🛒 **Coin-Shop System (Economy):** Shop where users can spend earned coins to purchase items, perks, or roles.

👥 **Bulk Role Management (Moderation):** Easily add or remove roles from multiple members at once.

📌 **Auto Thread Creator (Automation):** Automatically creates threads when users send messages in specific channels.

😄 **Auto Emoji Reactor (Automation):** Automatically reacts with predefined emojis to messages in selected channels.

⏰ **Scheduled Webhooks (Automation):** Sends pre-configured webhook messages on a defined schedule.

## 🤝 Contributing

We welcome contributions! Please check out our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact
- Join our community on **[Discord](https://discord.gg/pXaZdHpS5b)** to interact with other members and get updates.