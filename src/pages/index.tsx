import React, { JSX } from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/module-1-robotic-nervous-system/intro"
            style={{ marginRight: '1rem' }}>
            Start Module 1
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/module-2-digital-twin"
            style={{ marginRight: '1rem' }}>
            Start Module 2
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/module-3-ai-robot-brain"
            style={{ marginRight: '1rem' }}>
            Start Module 3
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/docs/module-4-vla">
            Start Module 4
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
