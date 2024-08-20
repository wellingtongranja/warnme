# Warnme

Warnme is a notification Python script that queries Snowflake and notifies a user via e-mail and SMS. 

## Prerequisites

- Python 3.x
- SMTP email account setup
- Snowflake account setup
- Twilio account setup

## Usage

1. **Clone the repository:**

    ```sh
    git clone https://github.com/wellingtongranja/warnme.git
    cd warnme
    ```

2. **Ensure you have a `requirements.txt` file in the root directory of the project.**

3. **Run warnme_setup.py to install required dependencies:**

    ```sh
    python warnme_setup.py
    ```

4. **Prepare your configuration files:**
    - Make sure you have the following configuration files in the `config` directory:
        - `sender_config.json`
        - `db_config.json`
        - `twilio_config.json`

5. **Prepare your query, CSS, and template files:**
    - Ensure you have the SQL query file, CSS file, and HTML template file ready.

6. **To run the script:**

    ```sh
    python warnme.py recipientEmail subject query cssFile templateFile outputFolder phoneNumber
    ```

    Example:

    ```sh
    python warnme.py "user@example.com" "Daily Report" "./queries/daily_report.sql" "./css/styles.css" "./templates/email_template.html" "./output" "+1234567890"
    ```

    *Phone number is optional for SMS notification.

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

## Credits

- [Snowflake](https://www.snowflake.com/) for providing the data warehouse service used in this project.
- Twilio for SMS notification services.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.
