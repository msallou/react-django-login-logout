import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import Layout from "./hocs/Layout";

import Home from "./containers/Home";
import Register from "./containers/Register";
import Login from "./containers/Login";
import Dashboard from "./containers/Dashboard";

import { Provider } from "react-redux";
import store from "./store";

const App = () => (
  <Provider store={store}>
    <Router>
      <Layout>
        <Routes>
          <Route exact path="/" Component={Home} />
          <Route exact path="/register" Component={Register} />
          <Route exact path="/login" Component={Login} />
          <Route exact path="/dashboard" Component={Dashboard} />
        </Routes>
      </Layout>
    </Router>
  </Provider>
);

export default App;
