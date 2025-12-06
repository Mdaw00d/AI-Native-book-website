import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import styles from './contact.module.css';

const LOCAL_STORAGE_KEY = 'physical_ai_waitlist';

export default function Contact(): JSX.Element {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    // Check if already on waitlist
    const savedEmail = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (savedEmail) {
      setEmail(savedEmail);
      setSubmitted(true);
      setMessage('You are already on the waitlist!');
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      localStorage.setItem(LOCAL_STORAGE_KEY, email);
      setSubmitted(true);
      setMessage('Thank you for joining the waitlist!');
    }
  };

  return (
    <Layout
      title="Contact Us"
      description="Get in touch with the Physical AI project team or join the waitlist."
    >
      <main className="container margin-vert--lg">
        <div className={clsx('row', styles.contactSection)}>
          <div className="col col--6 col--offset-3">
            <h1>Contact Us / Join Waitlist</h1>
            {!submitted ? (
              <form onSubmit={handleSubmit} className={styles.contactForm}>
                <div className="margin-bottom--md">
                  <label htmlFor="email" className="margin-right--sm">Email:</label>
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="your@example.com"
                    required
                    className={styles.inputField}
                  />
                </div>
                <button type="submit" className="button button--primary">Join Waitlist</button>
              </form>
            ) : (
              <div className={clsx('alert alert--success', styles.successMessage)}>
                <p>{message}</p>
                {email && <p>We will notify you at <strong>{email}</strong> when updates are available.</p>}
              </div>
            )}
            <p className="margin-top--md">
              For general inquiries, please reach out via our GitHub repository's issues section.
            </p>
          </div>
        </div>
      </main>
    </Layout>
  );
}
