# CBT System with Biometric Verification

This version integrates **face recognition** for biometric login.

## Features
- Register with face image (biometric encoding stored in memory)
- Login requires email, password, and face match
- Role-based dashboards (Admin, Student, Invigilator)

## Setup
1. Install system dependencies (Linux example):
   ```bash
   sudo apt-get update && sudo apt-get install -y cmake g++ libboost-all-dev
