import React from 'react';
import Layout from '@theme/Layout';

export default function About(): JSX.Element {
  return (
    <Layout
      title="About Physical AI"
      description="Learn about the Physical AI project and its teaching approach."
    >
      <main className="container margin-vert--lg">
        <h1>About Physical AI</h1>
        <p>
          The Physical AI project aims to provide comprehensive, book-style documentation
          for understanding and working with humanoid robotics, with a strong focus on
          the integration of AI. Our vision is to demystify complex robotics concepts
          and make them accessible to a broader audience, from students to professionals.
        </p>
        <p>
          Our teaching approach emphasizes practical examples, clear explanations, and a
          modular structure that allows learners to progress at their own pace. We believe
          in hands-on learning and provide the foundational knowledge necessary to build
          and experiment with physical AI systems.
        </p>
      </main>
    </Layout>
  );
}
