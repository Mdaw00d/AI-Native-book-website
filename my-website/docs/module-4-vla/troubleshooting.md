# Troubleshooting Guide

## Docker Issues

**Container won't start**
- Check Docker is running
- Verify 8GB+ RAM available
- Try: `docker-compose down && docker-compose up --build`

## ROS 2 Issues

**Nav2 server not available**
- Ensure simulation is running
- Check: `ros2 node list`

## LLM Issues

**OpenAI API errors**
- Verify API key in .env
- Check rate limits
- Alternative: Use Ollama locally

## Audio Issues

**Microphone not detected**
- Check permissions
- Verify device in system settings
- Try different audio backend
