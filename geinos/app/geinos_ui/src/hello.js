import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class hello extends Component {
    render() {
        return (
            <div className="hello">
                <header className="hello-header">
                    <img src={logo} className="hello-logo" alt="logo" />
                    <h1 className="hello-title">Welcome to React</h1>
                </header>
                <p className="hello-intro">
                    To get started, edit <code>src/App.js</code> and save to 1 reload.
                </p>
            </div>
        );
    }
}




export default hello;