import App from 'next/app'
import { AuthProvider } from '../contexts/AuthContext';
import React from 'react'
import { TaskProvider } from '../contexts/TaskContext';
import { Toaster } from 'react-hot-toast';

class MyApp extends App {
  render() {
    const { Component, pageProps } = this.props
    return (
      <AuthProvider><TaskProvider><Toaster/><Component {...pageProps} /></TaskProvider></AuthProvider>
    );
  }
}

export default MyApp;
