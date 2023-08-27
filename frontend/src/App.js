import { Container } from 'react-bootstrap'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import Header from './components/Header'
import Footer from './components/Footer'
import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <Router>
      <Header />
      <main classname='py-3'>
        <Container>
          <h1>Welcome!!!</h1>
        </Container>
      </main>
      <Footer />
    </Router>
  );
}

export default App;
