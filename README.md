# X (Twitter) Account Creation Bot

An automated bot for creating X (formerly Twitter) accounts using advanced browser fingerprinting and CAPTCHA solving techniques. This bot leverages the Castle.io fingerprinting library to generate realistic browser profiles and bypass security measures.

<p align="center">
  <img src="https://github.com/TomoeGozen82/twitter-account-creation-bot/blob/main/twitter-account-creation-bot.png" alt="Modern Tinder UI 2026" width="85%"/>

</p>

## ⚠️ Disclaimer

**This project is for educational and research purposes only.** Users are responsible for complying with X's Terms of Service and all applicable laws. The authors are not responsible for any misuse of this software.

## 🚀 Features

- **Automated Account Creation**: Complete X account signup process
- **Advanced Fingerprinting**: Uses Castle.io library for realistic browser profiles
- **CAPTCHA Solving**: Integrated Arkose Labs CAPTCHA solving via CDS Solver API
- **Proxy Support**: Built-in proxy usage capabilities
- **Realistic Data Generation**: Uses Faker library for authentic-looking profiles
- **Session Management**: Maintains proper session state throughout signup
- **Error Handling**: Comprehensive error handling and logging
- **Customizable**: Easy configuration for different use cases

## ⚙️ Configuration

### Advanced Usage

```python
# Create an API instance
bot = AccountCreationBot(
    email="your-email@example.com",
    proxy="http://proxy:port",
    username="desired_username"  # Optional, must be unique if provided
)

# Run the signup process
bot.signup()
```

## 📊 Account Creation Process

The bot follows this automated workflow:

1. **Guest Token Acquisition** - Obtains X API guest token
2. **JS Instrumentation** - Fetches browser fingerprinting data
3. **Signup Initialization** - Starts the account creation flow
4. **Profile Submission** - Submits user profile with Castle.io token
5. **Email Verification** - Handles email verification step
6. **Password Setup** - Sets account password with Castle.io token
7. **User Features** - Configures account features and settings
8. **Avatar Selection** - Skips avatar selection
9. **Username Setup** - Sets username
10. **Notifications** - Configures notification preferences
11. **Category Selection** - Selects account category
12. **User Recommendations** - Follows recommended accounts
13. **Flow Completion** - Finalizes account creation

## 📝 Logging

The bot provides comprehensive logging:

- **Console Output**: Real-time status updates
- **Log File**: Detailed logs saved to `log.txt`
- **Error Tracking**: Captures and logs all errors
- **Success Metrics**: Tracks successful account creation

## 🔍 Troubleshooting

### Common Issues

1. **CAPTCHA Solving Fails**
   - Verify CDS Solver API key is valid
   - Check API credits/balance
   - Ensure proxy is working (if used)

2. **Email Verification Issues**
   - Check email inbox for verification code
   - Ensure email address is valid and accessible
   - Try with different email provider

3. **Session Errors**
   - Check proxy configuration
   - Verify network connectivity

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Legal Notice

This software is provided for educational and research purposes only. Users must:

- Comply with X's Terms of Service
- Follow all applicable laws and regulations
- Use responsibly and ethically
- Not engage in spam or malicious activities

The authors are not responsible for any misuse of this software.

## 🙏 Acknowledgments

- [castleio-gen by yubie-re](https://github.com/yubie-re/castleio-gen)
- CDS Solver for CAPTCHA solving services
- Faker library for realistic data generation
- curl_cffi for HTTP client functionality

## 📞 Support

For questions or issues:

1. Check the [Issues](https://github.com/okoyausman/twitter-account-creation-bot/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Remember**: Always use this software responsibly and in compliance with all applicable terms of service and laws.
