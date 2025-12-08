---
sidebar_label: 'Chapter 4: ROS 2 Fundamentals - Part 3 (URDF)'
sidebar_position: 4
---

# Chapter 4: ROS 2 Fundamentals - Part 3 (URDF)

## Overview

Unified Robot Description Format (URDF) is an XML-based format used in ROS 2 to describe robot models. URDF defines the physical and visual properties of robots, including their kinematic structure, dynamics, and appearance. This chapter explores the fundamentals of robot modeling in ROS 2.

## What is URDF?

URDF (Unified Robot Description Format) is the standard format for representing robot models in ROS 2. It describes:

- **Kinematic structure**: How different parts of the robot are connected
- **Physical properties**: Mass, inertia, and collision geometry
- **Visual properties**: How the robot appears in simulation
- **Joint constraints**: Limits and ranges of motion
- **Sensor mounting points**: Where sensors are attached to the robot

## URDF Structure

### Links
Links represent rigid bodies in the robot. Each link has:
- **Visual**: How the link appears in visualization
- **Collision**: Geometry used for collision detection
- **Inertial**: Mass, center of mass, and inertia tensor

### Joints
Joints connect links and define their relative motion:
- **Fixed**: No relative motion between links
- **Revolute**: Single-axis rotation with limits
- **Continuous**: Single-axis rotation without limits
- **Prismatic**: Single-axis translation with limits
- **Floating**: Six degrees of freedom
- **Planar**: Motion on a plane

## Kinematic Chains

URDF models are organized as kinematic trees, with a single base link at the root. Each link is connected to its parent by exactly one joint, forming a tree structure that represents the robot's kinematic chain.

## URDF in Practice

### Xacro
Xacro (XML Macros) is an XML macro language that extends URDF with:
- **Macros**: Reusable components
- **Mathematical expressions**: Calculations in URDF
- **Properties**: Parameterized definitions
- **Inclusion**: Modular robot descriptions

### Robot State Publisher
The robot_state_publisher node reads URDF and joint positions to publish transforms for the robot's kinematic structure using TF2 (Transform Framework 2).

## Advanced URDF Features

### Transmission Elements
Define how actuators connect to joints, including:
- **Simple transmission**: Direct actuator-joint mapping
- **Differential transmission**: Differential drive mechanisms
- **Four-bar linkage**: Complex mechanical systems

### Gazebo Integration
URDF can include Gazebo-specific extensions for simulation:
- **Materials**: Visual appearance in Gazebo
- **Controllers**: Simulation-specific parameters
- **Sensors**: Simulation sensor models

## Learning Objectives

After completing this chapter, readers should be able to:
- Understand the structure and purpose of URDF in robot modeling
- Identify the key components of URDF: links, joints, and their properties
- Explain the role of Xacro in creating modular robot descriptions
- Recognize how URDF integrates with the ROS 2 ecosystem