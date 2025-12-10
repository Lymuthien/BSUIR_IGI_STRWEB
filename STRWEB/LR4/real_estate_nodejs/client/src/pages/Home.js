import React from 'react';
import { Link } from 'react-router-dom';
import DateTimeDisplay from '../components/DateTimeDisplay';
import MarketAnalyzer from '../components/MarketAnalyzer';
import PropertyMatcher from '../components/PropertyMatcher';
import '../styles/Home.css';

function Home() {
  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="container">
          <h1>Welcome to Real Estate Agency</h1>
          <p className="lead">Find your dream property with us</p>
          <Link to="/catalog" className="btn btn-primary btn-lg">
            Browse Properties
          </Link>
        </div>
      </section>

      <div className="container mt-5">
        <div className="row">
          <div className="col-md-12 mb-4">
            <DateTimeDisplay label="Current Time" />
          </div>
        </div>

        <div className="row">
          <div className="col-md-6 mb-4">
            <MarketAnalyzer />
          </div>
          <div className="col-md-6 mb-4">
            <PropertyMatcher />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;

