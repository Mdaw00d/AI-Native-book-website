// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

/** @type {import('@docusaurus/types').Config} */
const config = {
  url: "https://ai-native-book-website.vercel.app",
  baseUrl: "/",

  organizationName: "mdaw00ds", // optional, can keep
  projectName: "Physical-AI-Humanoids-Robotic-Textbook", // optional, can keep

  deploymentBranch: undefined, // or remove this line

  title: "Physical AI Documentation Book",
  tagline: "Master the Robotic Nervous System",
  favicon: "img/favicon.ico",

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          routeBasePath: "/docs",
        },
        blog: false,
        theme: {
          customCss: require.resolve("./src/css/index.css"),
        },
        sitemap: {
          changefreq: "weekly",
          priority: 0.5,
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: "img/docusaurus-social-card.jpg",
      navbar: {
        hideOnScroll: false,
        style: 'primary',
        title: "",
        logo: {
          alt: "Physical AI",
          src: "img/logo.jpg",
        },
        items: [],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Documentation",
            items: [
              {
                label: "Module 1: Robotic Nervous System",
                to: "/docs/intro",
              },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "About",
                to: "/about",
              },
              {
                label: "Contact",
                to: "/contact",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Documentation Book. Built with Docusaurus.`,
      },
      prism: {
        theme: require("prism-react-renderer").themes.github,
        darkTheme: require("prism-react-renderer").themes.vsDark,
      },
      colorMode: {
        defaultMode: "light",
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      docs: {
        sidebar: {
          hideable: true,
          autoCollapseCategories: true,
        },
      },
    }),

  plugins: [],
};

module.exports = config;
