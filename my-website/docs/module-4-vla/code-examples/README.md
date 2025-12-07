# VLA Integration Code Examples

This directory contains all code examples for the Vision-Language-Action (VLA) Integration module.

## Directory Structure

```
code-examples/
├── notebooks/          # Jupyter notebooks for interactive tutorials
│   ├── 01_voice_to_text.ipynb
│   ├── 02_llm_planning.ipynb
│   ├── 03_object_detection.ipynb
│   ├── 04_navigation.ipynb
│   └── 05_manipulation.ipynb
├── scripts/            # Standalone Python scripts
│   ├── voice_interface.py
│   ├── llm_planner.py
│   ├── object_detector.py
│   ├── navigation_client.py
│   ├── manipulation_primitives.py
│   └── full_pipeline.py
├── tests/              # Unit and integration tests
│   ├── test_voice_interface.py
│   ├── test_llm_planner.py
│   ├── test_object_detector.py
│   ├── test_navigation_client.py
│   ├── test_manipulation.py
│   └── test_integration.py
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed
- At least 8GB RAM available
- 4 CPU cores recommended

### Quick Start with Docker (Recommended)

1. **Build and start the container:**

```bash
# From project root
docker-compose up -d
```

2. **Enter the container:**

```bash
docker exec -it vla-ros2-simulation bash
```

3. **Install Python dependencies (if not already installed):**

```bash
cd /workspace/code-examples
pip3 install -r requirements.txt
```

4. **Set up environment variables:**

Create a `.env` file in `/workspace/code-examples/`:

```bash
# LLM API Key (for GPT-4)
OPENAI_API_KEY=your_api_key_here

# Optional: Local LLM endpoint (Ollama alternative)
# LOCAL_LLM_ENDPOINT=http://localhost:11434
```

**IMPORTANT**: Never commit `.env` files to Git. The API key is sensitive.

5. **Run Jupyter Lab (for notebooks):**

```bash
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Then access at `http://localhost:8888` (copy the token from terminal).

### Manual Installation (Advanced)

If you prefer not to use Docker:

1. **Install ROS 2 Humble:**
   - Follow official guide: https://docs.ros.org/en/humble/Installation.html

2. **Install Gazebo Garden:**
   - Follow official guide: https://gazebosim.org/docs/garden/install

3. **Install Nav2 and MoveIt 2:**

```bash
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-moveit
```

4. **Install Python dependencies:**

```bash
pip3 install -r requirements.txt
```

5. **Install system audio dependencies:**

```bash
sudo apt install ffmpeg portaudio19-dev
```

## Running Code Examples

### Jupyter Notebooks (Interactive Learning)

Notebooks are designed for step-by-step learning:

```bash
jupyter lab
# Navigate to notebooks/ folder
# Open and run cells sequentially
```

### Standalone Scripts

Scripts demonstrate production-ready code:

```bash
# Voice interface example
python3 scripts/voice_interface.py --audio-file test.wav

# LLM planning example
python3 scripts/llm_planner.py --command "Navigate to the kitchen"

# Object detection example
python3 scripts/object_detector.py --image test_image.jpg

# Full pipeline (requires ROS 2 simulation running)
python3 scripts/full_pipeline.py --command "Pick up the red cup"
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=scripts --cov-report=html

# Specific test file
pytest tests/test_llm_planner.py -v
```

## Troubleshooting

### Docker Issues

**Problem**: Container fails to start
**Solution**: Check Docker logs: `docker-compose logs`

**Problem**: Gazebo GUI doesn't appear
**Solution**:
- On Linux: `xhost +local:docker` before starting container
- On macOS: Install XQuartz and set DISPLAY variable
- On Windows: Use WSL2 with X server (VcXsrv)

### ROS 2 Issues

**Problem**: `ros2` command not found
**Solution**: Source ROS setup: `source /opt/ros/humble/setup.bash`

**Problem**: Nav2 navigation fails
**Solution**: Ensure Gazebo world is loaded and robot is spawned

### Python Issues

**Problem**: `ModuleNotFoundError` for ROS packages
**Solution**: Install via apt, not pip: `sudo apt install ros-humble-<package>`

**Problem**: Whisper transcription too slow
**Solution**: Use smaller model: `whisper.load_model("base")` instead of "large"

### LLM Issues

**Problem**: OpenAI API rate limit exceeded
**Solution**:
- Add retry logic with exponential backoff
- Switch to local LLM (Ollama + Llama 3.1)
- Use smaller/faster model (gpt-3.5-turbo)

**Problem**: LLM output doesn't match JSON schema
**Solution**:
- Use GPT-4 with `response_format={"type": "json_object"}`
- Add JSON schema validation and retry
- Check prompt for clarity

## Additional Resources

- **ROS 2 Humble Docs**: https://docs.ros.org/en/humble/
- **Nav2 Documentation**: https://navigation.ros.org/
- **MoveIt 2 Tutorials**: https://moveit.ros.org/
- **Whisper GitHub**: https://github.com/openai/whisper
- **YOLOv8 Docs**: https://docs.ultralytics.com/

## Support

For issues or questions:
1. Check the troubleshooting guide above
2. Review module documentation in `docs/module-4-vla/`
3. Open an issue on GitHub

---

**Last Updated**: 2025-12-07
**Module**: Vision-Language-Action (VLA) Integration
