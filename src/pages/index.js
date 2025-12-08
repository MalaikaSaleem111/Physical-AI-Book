import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Read the Book
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="A comprehensive guide to Physical AI and humanoid robotics fundamentals">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <h3>Physical AI Foundations</h3>
                <p>Learn the fundamentals of Physical AI and embodied intelligence.</p>
              </div>
              <div className="col col--4">
                <h3>Simulation & Development</h3>
                <p>Explore ROS 2 concepts and simulation environments.</p>
              </div>
              <div className="col col--4">
                <h3>Advanced Systems</h3>
                <p>Discover NVIDIA Isaac platform and Vision-Language-Action systems.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}