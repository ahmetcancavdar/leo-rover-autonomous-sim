#!/usr/bin/env python3
import os

def generate_world():
    world_content = """<?xml version="1.0"?>
<sdf version="1.6">
  <world name="default">
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>
    <plugin name="gazebo_ros_state" filename="libgazebo_ros_state.so">
      <ros>
        <namespace>/gazebo</namespace>
      </ros>
    </plugin>
    <include>
      <uri>model://sun</uri>
    </include>
    <model name="solid_ground">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
            <specular>0.1 0.1 0.1 1</specular>
          </material>
        </visual>
      </link>
      <plugin filename="libignition-gazebo-grid-system.so"
        name="ignition::gazebo::systems::Grid">
        <cell_length>1.0</cell_length>
        <cell_count>20</cell_count>
        <vertical_cell_count>20</vertical_cell_count>
        <horizontal_cell_count>20</horizontal_cell_count>
        <color>0 0 0 1</color>
        <ambient>0 0 0 1</ambient>
        <!-- Offset the grid lines so that intersections occur exactly at integer values -->
        <pose>0 0 0.001 0 0 0</pose>
      </plugin>
    </model>
"""

    # Add visual coordinate markers for every integer cross
    for x in range(-10, 11):
        for y in range(-10, 11):
            
            # Determine color and size
            if x == 0 and y == 0:
                # Origin (0,0) is a larger BLUE box
                color = "0 0 1 1"
                shape = f"""<box><size>0.2 0.2 0.02</size></box>"""
            elif y == 0:
                # X axis is a RED rect
                color = "1 0 0 1"
                shape = f"""<box><size>0.8 0.05 0.02</size></box>"""
            elif x == 0:
                # Y axis is a GREEN rect
                color = "0 1 0 1"
                shape = f"""<box><size>0.05 0.8 0.02</size></box>"""
            else:
                # Normal grid point is a small white/grey box
                color = "0.2 0.2 0.2 1"
                shape = f"""<box><size>0.1 0.1 0.01</size></box>"""

            world_content += f"""
    <model name="marker_{x}_{y}">
      <static>true</static>
      <pose>{x} {y} 0.01 0 0 0</pose>
      <link name="link">
        <visual name="visual">
          <geometry>
            {shape}
          </geometry>
          <material>
            <ambient>{color}</ambient>
            <diffuse>{color}</diffuse>
          </material>
        </visual>
      </link>
    </model>
"""
    
    world_content += """
  </world>
</sdf>
"""

    world_path = '/home/ahmetcan/Masaüstü/antiotonom/ros2_ws/src/leo_nav_custom/worlds/flat_empty.world'
    os.makedirs(os.path.dirname(world_path), exist_ok=True)
    with open(world_path, 'w') as f:
        f.write(world_content)
    print(f"Generated {world_path}")

if __name__ == '__main__':
    generate_world()
