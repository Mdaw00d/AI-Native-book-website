import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import CustomLayout from '@site/src/components/CustomLayout';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@site/src/components/shadcn-ui/Card';
import { Button } from '@site/src/components/shadcn-ui/Button';
import FeatureIcon from '@site/src/components/FeatureIcon';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className="relative bg-gradient-to-br from-[#0077FF] via-[#00D9FF] to-[#00C9A7] dark:from-[#0A192F] dark:via-[#0077FF] dark:to-[#00D9FF] text-white py-20 overflow-hidden">
      {/* Glassmorphism overlay with tech glow */}
      <div className="absolute inset-0 backdrop-blur-sm bg-white/5"></div>
      {/* Tech grid pattern overlay */}
      <div className="absolute inset-0 opacity-10" style={{
        backgroundImage: 'linear-gradient(rgba(0, 217, 255, 0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 217, 255, 0.3) 1px, transparent 1px)',
        backgroundSize: '40px 40px'
      }}></div>
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-5xl font-bold mb-4 drop-shadow-2xl" style={{textShadow: '0 0 30px rgba(0, 217, 255, 0.5)'}}>{siteConfig.title}</h1>
          <p className="text-xl mb-8 text-white/90 drop-shadow-lg">{siteConfig.tagline}</p>
          <div className="flex gap-4 justify-center">
            <Link to="/docs/intro">
              <Button size="lg" className="bg-white/20 backdrop-blur-md border-[#00D9FF]/30 text-white hover:bg-white/30 shadow-[0_0_20px_rgba(0,217,255,0.3)] hover:shadow-[0_0_30px_rgba(0,217,255,0.5)] transition-all duration-300 hover:scale-105">
                Get Started
              </Button>
            </Link>
            <Link to="/about">
              <Button variant="outline" size="lg" className="border-white/40 bg-white/10 backdrop-blur-md text-white hover:bg-white/20 shadow-[0_0_15px_rgba(0,119,255,0.2)] hover:shadow-[0_0_25px_rgba(0,217,255,0.4)] transition-all duration-300 hover:scale-105">
                Learn More
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

function PhysicalAIIntro() {
  return (
    <section className="py-16 px-4">
      <div className="container mx-auto max-w-4xl">
        <h2 className="text-3xl font-bold text-center mb-8 bg-gradient-to-r from-[#0077FF] via-[#00D9FF] to-[#00C9A7] bg-clip-text text-transparent dark:from-[#00D9FF] dark:via-[#7FD8FF] dark:to-[#00C9A7]">What is Physical AI?</h2>
        <p className="text-lg text-center mb-6 text-gray-700 dark:text-gray-300">
          Physical AI represents the convergence of artificial intelligence with the physical world.
          It's where robots don't just compute—they perceive, reason, and act in real environments.
        </p>
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardHeader className="text-center">
              <div className="mb-4 flex justify-center">
                <FeatureIcon type="eye" />
              </div>
              <CardTitle className="text-xl">Perceive</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p>Sensors capture the physical environment: cameras see, LIDAR measures distance, IMUs track orientation.</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="text-center">
              <div className="mb-4 flex justify-center">
                <FeatureIcon type="brain" />
              </div>
              <CardTitle className="text-xl">Process</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p>AI algorithms interpret sensor data, make decisions, and plan actions using neural networks and ML models.</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="text-center">
              <div className="mb-4 flex justify-center">
                <FeatureIcon type="gear" />
              </div>
              <CardTitle className="text-xl">Act</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p>Actuators and motors execute commands, moving limbs, gripping objects, and navigating spaces.</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}

function ModuleOverview() {
  const modules = [
    {
      title: 'Module 1: The Robotic Nervous System',
      description: 'Master ROS 2, the communication backbone of modern robotics. Learn nodes, topics, services, and robot modeling with URDF.',
      chapters: 4,
      link: '/docs/module-01-robotic-nervous-system/ros-middleware',
      topics: ['ROS 2 Middleware', 'Nodes & Topics', 'Python rclpy', 'URDF Modeling'],
    },
    {
      title: 'Module 2: The Digital Twin',
      description: 'Create realistic digital twins with Gazebo and Unity. Learn physics simulation, environment building, and sensor modeling.',
      chapters: 4,
      link: '/docs/module-02-digital-twin',
      topics: ['Gazebo Physics', 'Building Environments', 'Unity Rendering', 'Sensor Simulation'],
    },
    {
      title: 'Module 3: The AI-Robot Brain',
      description: 'Advanced perception, simulation training, and navigation pipelines for bipedal humanoid robots using NVIDIA Isaac technologies.',
      chapters: 4,
      link: '/docs/module-03-ai-robot-brain',
      topics: ['Isaac Sim & Synthetic Data', 'Isaac ROS Perception', 'Visual SLAM', 'Nav2 Planning'],
    },
    {
      title: 'Module 4: Vision-Language-Action',
      description: 'Integrate voice commands, LLM planning, and computer vision to build autonomous humanoid robots that understand language and interact with the world.',
      chapters: 5,
      link: '/docs/module-04-vision-language-action',
      topics: ['Voice-to-Action (Whisper)', 'Cognitive Planning (LLMs)', 'Computer Vision (CLIP/SAM/DINO)', 'Capstone: Autonomous Humanoid'],
    },
  ];

  return (
    <section className="py-16 px-4 bg-gray-50 dark:bg-gray-900 relative" style={{ marginTop: '2rem', marginBottom: '2rem' }}>
      {/* Subtle tech grid background */}
      <div className="absolute inset-0 opacity-5" style={{
        backgroundImage: 'linear-gradient(rgba(0, 119, 255, 0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 119, 255, 0.3) 1px, transparent 1px)',
        backgroundSize: '32px 32px'
      }}></div>
      <div className="container mx-auto max-w-6xl relative">
        <h2 className="text-3xl font-bold text-center mb-12 bg-gradient-to-r from-[#0077FF] via-[#00D9FF] to-[#00C9A7] bg-clip-text text-transparent dark:from-[#00D9FF] dark:via-[#7FD8FF] dark:to-[#00C9A7]">Available Modules</h2>
        <div className="grid md:grid-cols-1 gap-8">
          {modules.map((module, idx) => (
            <Card key={idx}>
              <CardHeader>
                <CardTitle className="text-2xl">{module.title}</CardTitle>
                <CardDescription className="text-base mt-2">
                  {module.description}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="mb-4">
                  <p className="font-semibold mb-2">Topics Covered:</p>
                  <ul className="list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
                    {module.topics.map((topic, topicIdx) => (
                      <li key={topicIdx}>{topic}</li>
                    ))}
                  </ul>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {module.chapters} chapters
                  </span>
                  <Link to={module.link}>
                    <Button>Start Module →</Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

function Features() {
  const features = [
    {
      title: 'Interactive Examples',
      description: 'Copy-paste code samples with syntax highlighting. Run them in your own environment.',
      icon: 'code',
    },
    {
      title: 'Visual Diagrams',
      description: 'Complex concepts explained with clear illustrations, flowcharts, and animations.',
      icon: 'diagram',
    },
    {
      title: 'Practical Projects',
      description: 'Hands-on exercises reinforce learning. Build real robots, not just theory.',
      icon: 'robot',
    },
    {
      title: 'Best Practices',
      description: 'Industry-standard approaches from professionals building production robots.',
      icon: 'sparkle',
    },
    {
      title: 'Progressive Learning',
      description: 'Start from fundamentals, build to advanced topics. Each chapter prepares you for the next.',
      icon: 'book',
    },
    {
      title: 'Always Updated',
      description: 'Documentation evolves with the field. Latest tools, techniques, and frameworks.',
      icon: 'refresh',
    },
  ];

  return (
    <section className="py-16 px-4">
      <div className="container mx-auto max-w-6xl">
        <h2 className="text-3xl font-bold text-center mb-12 bg-gradient-to-r from-[#0077FF] via-[#00D9FF] to-[#00C9A7] bg-clip-text text-transparent dark:from-[#00D9FF] dark:via-[#7FD8FF] dark:to-[#00C9A7]">Why This Documentation?</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, idx) => (
            <Card key={idx}>
              <CardHeader className="text-center">
                <div className="mb-4 flex justify-center">
                  <FeatureIcon type={feature.icon} />
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p>{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

function CallToAction() {
  return (
    <section className="relative py-16 px-4 bg-gradient-to-r from-[#00C9A7] via-[#00D9FF] to-[#0077FF] dark:from-[#0077FF] dark:via-[#00D9FF] dark:to-[#00C9A7] text-white overflow-hidden">
      {/* Glassmorphism overlay */}
      <div className="absolute inset-0 backdrop-blur-sm bg-white/5"></div>
      {/* Tech circuit pattern overlay */}
      <div className="absolute inset-0 opacity-10" style={{
        backgroundImage: 'linear-gradient(rgba(255, 255, 255, 0.2) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.2) 1px, transparent 1px)',
        backgroundSize: '50px 50px'
      }}></div>
      <div className="relative container mx-auto max-w-4xl text-center">
        <h2 className="text-3xl font-bold mb-4 drop-shadow-lg" style={{textShadow: '0 0 25px rgba(0, 217, 255, 0.6)'}}>Ready to Build Intelligent Robots?</h2>
        <p className="text-xl mb-8 text-white/90 drop-shadow-md">
          Start with Module 1 and master the foundation of Physical AI. From ROS 2 basics to robot modeling,
          you'll gain the skills to create sophisticated robotic systems.
        </p>
        <Link to="/docs/intro">
          <Button variant="default" size="lg" className="bg-white/20 backdrop-blur-md border-[#00D9FF]/30 text-white hover:bg-white/30 shadow-[0_0_20px_rgba(0,217,255,0.4)] hover:shadow-[0_0_35px_rgba(0,217,255,0.6)] transition-all duration-300 hover:scale-105">
            Begin Your Journey →
          </Button>
        </Link>
      </div>
    </section>
  );
}

export default function Home() {
  return (
    <CustomLayout>
      <HomepageHeader />
      <PhysicalAIIntro />
      <ModuleOverview />
      <Features />
      <CallToAction />
    </CustomLayout>
  );
}
