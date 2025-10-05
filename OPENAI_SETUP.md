# OpenAI API Setup for Bridgette

## Why is the OpenAI API needed?

The download button uses OpenAI's ChatGPT API to intelligently analyze and match schemas between different banks. This allows the system to:

1. **Intelligently match schemas** between Bank 1 and Bank 2 data
2. **Create meaningful relationships** between different data fields
3. **Generate a unified Excel file** with properly mapped data

## How to set up the OpenAI API key

### Option 1: Using a .env file (Recommended)

1. Create a `.env` file in the root directory of your project
2. Add your OpenAI API key:

```env
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### Option 2: Using environment variables

Set the environment variable in your system:

**Windows:**
```cmd
set OPENAI_API_KEY=your_actual_openai_api_key_here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY=your_actual_openai_api_key_here
```

## Getting an OpenAI API key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to the API section
4. Create a new API key
5. Copy the key and add it to your `.env` file

## Fallback functionality

If you don't have an OpenAI API key, the system will still work but with limited functionality:

- ✅ **Files will be processed** and converted to JSON
- ✅ **A basic Excel file will be created** with all data combined
- ❌ **No intelligent schema matching** will occur
- ❌ **No AI-powered data analysis** will be performed

## Cost considerations

- OpenAI API usage is charged per token
- For typical bank schema analysis, costs are usually under $1-5 per analysis
- You can set usage limits in your OpenAI account

## Troubleshooting

If you're still having issues:

1. **Check your API key** is correctly set in the `.env` file
2. **Restart the backend server** after adding the API key
3. **Check the console logs** for any error messages
4. **Verify your OpenAI account** has sufficient credits

## Need help?

If you need assistance setting up the OpenAI API, please contact the development team.
