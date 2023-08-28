import { render } from "react-dom";
import React from 'react';
import logo from './logo.svg';
import './App.css';


import { Container } from "react-bootstrap";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import HomeScreen from "./screens/HomeScreen";
import RecipeScreen from "./screens/RecipeScreen";

function App() {
  return (
    <Router>
      <Header />

      <main className="py-3">
        <Container>
          <Routes>

            <Route path="/" element={<HomeScreen />} exact />
            <Route path="/home" element={<HomeScreen />} exact />
            <Route path="/recipe/:id" element={<RecipeScreen />} />

            <Route path="*" element={
                <div style={{ padding: "1rem" }}>
                  <p>There's nothing here!</p>
                </div>} />

          </Routes>
        </Container>
      </main>

      <Footer />
    </Router>
  );
}

export default App;