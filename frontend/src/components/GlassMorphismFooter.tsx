import React from 'react';

const GlassMorphismFooter = () => {
  // Documentation modules with their sub-items
  const documentationModules = [
    {
      title: "Module 1: The Robotic Nervous System",
      items: [
        { label: "ROS Middleware", href: "/docs/module-01-robotic-nervous-system/ros-middleware" },
        { label: "Nodes, Topics & Services", href: "/docs/module-01-robotic-nervous-system/nodes-topics-services" },
        { label: "Python rclpy Bridge", href: "/docs/module-01-robotic-nervous-system/python-rclpy-bridge" },
        { label: "URDF Humanoids", href: "/docs/module-01-robotic-nervous-system/urdf-humanoids" },
      ]
    },
    {
      title: "Module 2: The Digital Twin",
      items: [
        { label: "Digital Twin Overview", href: "/docs/module-02-digital-twin/module-02-digital-twin" },
        { label: "Gazebo Physics Simulation", href: "/docs/module-02-digital-twin/gazebo-physics-simulation" },
        { label: "Building Environments", href: "/docs/module-02-digital-twin/building-environments" },
        { label: "Unity Rendering & Interaction", href: "/docs/module-02-digital-twin/unity-rendering-interaction" },
        { label: "Sensor Simulation", href: "/docs/module-02-digital-twin/sensor-simulation" },
      ]
    },
    {
      title: "Module 3: The AI-Robot Brain",
      items: [
        { label: "AI-Robot Brain Overview", href: "/docs/module-03-ai-robot-brain/module-03-ai-robot-brain" },
        { label: "Isaac Sim Synthetic Data", href: "/docs/module-03-ai-robot-brain/isaac-sim-synthetic-data" },
        { label: "Isaac ROS Perception", href: "/docs/module-03-ai-robot-brain/isaac-ros-perception" },
        { label: "Visual SLAM Navigation", href: "/docs/module-03-ai-robot-brain/visual-slam-navigation" },
        { label: "Nav2 Bipedal Planning", href: "/docs/module-03-ai-robot-brain/nav2-bipedal-planning" },
      ]
    },
    {
      title: "Module 4: Vision-Language-Action",
      items: [
        { label: "Module 4 Introduction", href: "/docs/module-04-vision-language-action/module-04-intro" },
        { label: "Capstone: Autonomous Humanoid", href: "/docs/module-04-vision-language-action/capstone-autonomous-humanoid" },
        { label: "Cognitive Planning with LLMs", href: "/docs/module-04-vision-language-action/cognitive-planning-llms" },
        { label: "Computer Vision & Object Recognition", href: "/docs/module-04-vision-language-action/computer-vision-object-recognition" },
        { label: "Voice to Action with Whisper", href: "/docs/module-04-vision-language-action/voice-to-action-whisper" },
        { label: "Chapter 1 Completion", href: "/docs/module-04-vision-language-action/chapter1-completion" },
      ]
    }
  ];

  const quickLinks = [
    { label: "Documentation", href: "/docs/intro" },
    { label: "About", href: "/about" },
    { label: "Contact", href: "/contact" },
  ];

  const resources = [
    { label: "Get Started", href: "/docs/intro" },
    { label: "GitHub Repository", href: "https://github.com/maryumxx/Physical-AI-Humanoids-Robotic-Textbook" },
    { label: "Docusaurus", href: "https://docusaurus.io" },
  ];

  return (
    <footer className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-t border-[#00D9FF]/20 dark:border-[#00D9FF]/30 py-12 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Project Info */}
          <div className="lg:col-span-2">
            <h3 className="text-xl font-bold bg-gradient-to-r from-[#0077FF] via-[#00D9FF] to-[#00C9A7] bg-clip-text text-transparent dark:from-[#00D9FF] dark:via-[#7FD8FF] dark:to-[#00C9A7] mb-4">
              Physical AI Documentation
            </h3>
            <p className="text-gray-700 dark:text-gray-300 mb-4">
              Master the Robotic Nervous System and build intelligent robots with our comprehensive documentation covering everything from ROS fundamentals to advanced AI-robotics integration.
            </p>
            <div className="flex space-x-4">
              <a
                href="https://github.com/maryumxx/Physical-AI-Humanoids-Robotic-Textbook"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 dark:text-gray-400 hover:text-[#00D9FF] dark:hover:text-[#00D9FF] transition-colors duration-300"
                aria-label="GitHub Repository"
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
          </div>

          {/* Documentation Modules */}
          <div>
            <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Documentation</h4>
            <ul className="space-y-2">
              <li>
                <a
                  href="/docs/intro"
                  className="text-gray-600 dark:text-gray-300 hover:text-[#00D9FF] dark:hover:text-[#00D9FF] transition-colors duration-300"
                >
                  Introduction
                </a>
              </li>
              {documentationModules.map((module, index) => (
                <li key={index} className="ml-4">
                  <details className="group">
                    <summary className="cursor-pointer text-gray-600 dark:text-gray-300 hover:text-[#00D9FF] dark:hover:text-[#00D9FF] transition-colors duration-300 list-none">
                      <span className="inline-block">{module.title}</span>
                      <span className="ml-2 group-open:rotate-180 transition-transform duration-200">▼</span>
                    </summary>
                    <ul className="mt-2 ml-4 space-y-1">
                      {module.items.map((item, itemIndex) => (
                        <li key={itemIndex}>
                          <a
                            href={item.href}
                            className="text-gray-500 dark:text-gray-400 hover:text-[#0077FF] dark:hover:text-[#0077FF] text-sm transition-colors duration-300 block"
                          >
                            {item.label}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </details>
                </li>
              ))}
            </ul>
          </div>

          {/* Quick Links and Resources */}
          <div>
            <div className="mb-6">
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Links</h4>
              <ul className="space-y-2">
                {quickLinks.map((link, index) => (
                  <li key={index}>
                    <a
                      href={link.href}
                      className="text-gray-600 dark:text-gray-300 hover:text-[#00D9FF] dark:hover:text-[#00D9FF] transition-colors duration-300"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Resources</h4>
              <ul className="space-y-2">
                {resources.map((resource, index) => (
                  <li key={index}>
                    <a
                      href={resource.href}
                      className="text-gray-600 dark:text-gray-300 hover:text-[#00D9FF] dark:hover:text-[#00D9FF] transition-colors duration-300"
                    >
                      {resource.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="border-t border-[#00D9FF]/20 dark:border-[#00D9FF]/30 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              © {new Date().getFullYear()} Physical AI Documentation Book. Built with Docusaurus.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a
                href="/privacy"
                className="text-gray-500 dark:text-gray-400 hover:text-[#00D9FF] dark:hover:text-[#00D9FF] text-sm transition-colors duration-300"
              >
                Privacy Policy
              </a>
              <a
                href="/terms"
                className="text-gray-500 dark:text-gray-400 hover:text-[#00D9FF] dark:hover:text-[#00D9FF] text-sm transition-colors duration-300"
              >
                Terms of Service
              </a>
              <a
                href="/contact"
                className="text-gray-500 dark:text-gray-400 hover:text-[#00D9FF] dark:hover:text-[#00D9FF] text-sm transition-colors duration-300"
              >
                Contact
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default GlassMorphismFooter;