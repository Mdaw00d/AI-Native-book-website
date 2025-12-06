import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'ROS 2 Middleware',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Explore the core communication mechanisms of ROS 2, including DDS (Data Distribution Service)
        and Quality of Service (QoS) policies.
      </>
    ),
  },
  {
    title: 'Nodes, Topics, and Services',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Understand the fundamental building blocks of a ROS graph: nodes as computational units,
        topics for asynchronous data streaming, and services for synchronous request/response patterns.
      </>
    ),
  },
  {
    title: 'Python-to-ROS Bridging with rclpy',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Learn how to write ROS 2 applications using Python with the `rclpy` client library, enabling
        seamless integration of Python scripts into the ROS ecosystem.
      </>
    ),
  },
  {
    title: 'URDF Modeling for Humanoid Robots',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Dive into the Unified Robot Description Format (URDF) to model humanoid robot kinematics
        and visualize their structure in ROS 2.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4', styles.featureItem)}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <h2 className="text--center">Module 1: The Robotic Nervous System (ROS 2)</h2>
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
