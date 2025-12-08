// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A comprehensive guide to Physical AI and humanoid robotics fundamentals',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://MalaikaSaleem111.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub Pages deployment with docs folder, use '/<organization-name>/<repo-name>/docs/'
  baseUrl: '/Physical-AI-Book/docs/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'MalaikaSaleem111', // Usually your GitHub org/user name.
  projectName: 'Physical-AI-Book', // Usually your repo name.

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: false, // Disable blog functionality
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Physical AI Logo',
          src: '/img/logo.svg',
          href: '/docs/intro',
          
          
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            href: 'https://github.com/MalaikaSaleem111/Physical-AI-Book.git',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Content',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
              {
                label: 'Part I: Foundations',
                to: '/docs/chapter-01-introduction-to-physical-ai',
              },
              {
                label: 'Part II: Digital Twin & Simlation',
                to: '/docs/chapter-05-digital-twin-simulation-part1',
              },
              {
                label: 'part III: NVIDIA Isaac Platform',
                to: '/docs/chapter-07-nvidia-isaac-sim-perception',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'GitHub Repository',
                href: 'https://github.com/MalaikaSaleem111/Physical-AI-Book.git',
              },
              {
                label: 'NVIDIA Isaac',
                href: 'https://developer.nvidia.com/isaac-sim',
              },
              {
                label: 'ROS 2 Documentation',
                href: 'https://docs.ros.org/en/humble/',
              },
            ],
          },
         
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Book. Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;