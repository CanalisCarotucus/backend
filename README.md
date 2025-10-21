# Pinkman

This is simple template without database, reddis and other technologies for fast development.

## Project Structure
```
├── app/                        # Main application directory
│   ├── config/                 # Configuration files
│   │   └── config.py           # Main configuration file
│   ├── middlewares/            # Middleware components
│   │   └── log.py              # Logging middleware
│   ├── models/                 # Data models
│   │   └── hello_world.py      # Example model
│   ├── routers/                # API route definitions
│   │   └── hello_world.py      # Example route
├── main.py                     # Main application file
├── .env                        # Environment variables
├── requests.log                # Log of requests made
├── pyproject.toml              # List of Python dependencies
├── run.sh                      # Script to run the application
└── README.md                   # Project documentation
```

### Prerequisites
- Python 3.10+

1. **Clone repository**  
   Run the following command to download project:  
   ```bash
   git clone -b simple https://github.com/iismoilov7/pinkman.git
   cd pinkman
   ```

2. **Install Required Packages**  
   Run the following command to install the necessary dependencies:  
   ```bash
   uv sync
   ```

3. **Create a `.env` file**
   Create a `.env` file in the project root, you can use `.env-example` for instacne

4. **Start the Application**  
   Launch the application with the following command:  
   ```bash
   bash run.sh
   ```
