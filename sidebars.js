// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Part I: Foundations',
      items: [
        'chapter-01-introduction-to-physical-ai/index',
        'chapter-02-ros2-fundamentals/index',
        'chapter-03-ros2-fundamentals-part2/index',
        'chapter-04-ros2-fundamentals-part3/index'
      ],
      collapsed: false
    },
    {
      type: 'category',
      label: 'Part II: Digital Twin & Simulation',
      items: [
        'chapter-05-digital-twin-simulation-part1/index',
        'chapter-06-digital-twin-simulation-part2/index'
      ],
      collapsed: false
    },
    {
      type: 'category',
      label: 'Part III: NVIDIA Isaac Platform',
      items: [
        'chapter-07-nvidia-isaac-sim-perception/index',
        'chapter-08-nvidia-isaac-sim-vslam-nav2/index',
        'chapter-09-nvidia-isaac-sim-rl-basics/index'
      ],
      collapsed: false
    },
    {
      type: 'category',
      label: 'Part IV: Humanoid Robotics',
      items: [
        'chapter-10-humanoid-kinematics/index',
        'chapter-11-humanoid-locomotion-manipulation/index',
        'chapter-12-vision-language-action/index',
        'chapter-13-capstone-concept/index',
        'chapter-14-humanoid-control-systems/index'
      ],
      collapsed: false
    },
    {
      type: 'category',
      label: 'Part V: Supporting Content',
      items: [
        'chapter-15-hardware-overview/index',
        'chapter-16-robot-lab-options/index',
        'chapter-17-cloud-compute-options/index',
        {
          type: 'category',
          label: 'Appendices',
          items: [
            'appendices/architecture-diagrams/index',
            'appendices/references/index',
            'appendices/diagrams/index'
          ],
          collapsed: true
        }
      ],
      collapsed: false
    },
    {
      type: 'category',
      label: 'Part VI: Weekly Learning Modules & Outcomes',
      items: [
        'chapter-18-weekly-breakdown/index',
        'chapter-19-learning-outcomes/index'
      ],
      collapsed: false
    }
  ]
};

export default sidebars;