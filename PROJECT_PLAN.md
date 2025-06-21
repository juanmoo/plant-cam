# Project Planning – PlantCam

## Goal
Automatically collect plant images and generate timelapse videos via a web interface.

## Components
### 1. Raspberry Pi Data Collector
- Capture and upload photos periodically

### 2. Server Backend (Python)
- Receive/store images
- Expose API for video generation/listing
- Efficient storage & indexing

### 3. Time Lapse Video Generator
- Generate videos by time range, FPS, video duration
- Optimize for speed from possibly large image sets

### 4. Web Frontend
- Simple interface for selecting time ranges and video options
- Preview or download final videos

## Storage
- Images organized by timestamp and device

## Requirements
- Hourly upload latency max
- Fast, responsive video generation

## Milestones
- Pi upload + backend storage
- Video generation API & UI
- Final optimization
