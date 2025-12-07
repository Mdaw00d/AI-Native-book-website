import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI: Humanoid Robotics',
  tagline: 'A comprehensive guide to building intelligent humanoid robots with ROS 2, computer vision, and machine learning',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://physical-ai-book.example.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub Pages deployment config
  organizationName: 'your-org',
  projectName: 'physical-ai-book',

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // SEO metadata
  headTags: [
    {
      tagName: 'meta',
      attributes: {
        name: 'keywords',
        content: 'robotics, humanoid robots, ROS 2, physical AI, machine learning, computer vision, URDF, rclpy, robot operating system',
      },
    },
    {
      tagName: 'meta',
      attributes: {
        name: 'author',
        content: 'Physical AI Team',
      },
    },
    {
      tagName: 'meta',
      attributes: {
        property: 'og:type',
        content: 'website',
      },
    },
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Remove edit this page links for now
          editUrl: undefined,
          // Show last update info
          showLastUpdateAuthor: false,
          showLastUpdateTime: true,
          // Breadcrumbs
          breadcrumbs: true,
        },
        blog: false, // Disable blog for now
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',

    // Enhanced metadata
    metadata: [
      {name: 'description', content: 'Learn to build intelligent humanoid robots with comprehensive tutorials on ROS 2, computer vision, machine learning, and robot kinematics.'},
      {name: 'og:description', content: 'Learn to build intelligent humanoid robots with comprehensive tutorials on ROS 2, computer vision, machine learning, and robot kinematics.'},
      {name: 'twitter:card', content: 'summary_large_image'},
    ],

    // Color mode configuration
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },

    // Docs-only mode configuration
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: false,
      },
    },

    // Navigation bar
    navbar: {
      title: 'Physical AI',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      hideOnScroll: false,
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Modules',
        },
        {
          to: '/about',
          label: 'About',
          position: 'left',
        },
        {
          to: '/contact',
          label: 'Contact',
          position: 'left',
        },
        {
          type: 'search',
          position: 'right',
        },
      ],
    },

    // Algolia search (placeholder - requires Algolia setup)
    // algolia: {
    //   appId: 'YOUR_APP_ID',
    //   apiKey: 'YOUR_SEARCH_API_KEY',
    //   indexName: 'physical-ai',
    //   contextualSearch: true,
    // },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            {
              label: 'Module 1: ROS 2 Fundamentals',
              to: '/docs/module-1-robotic-nervous-system/intro',
            },
            {
              label: 'Getting Started',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'ROS 2 Documentation',
              href: 'https://docs.ros.org/en/humble/',
            },
            {
              label: 'Gazebo Simulator',
              href: 'https://gazebosim.org/',
            },
            {
              label: 'OpenCV',
              href: 'https://opencv.org/',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'About',
              to: '/about',
            },
            {
              label: 'Contact',
              to: '/contact',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Book. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'cpp', 'cmake', 'yaml', 'json'],
    },

    // Table of contents settings
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },
  } satisfies Preset.ThemeConfig,
};

  config.clientModules = [require.resolve('./src/theme/Root.tsx')];

export default config;
