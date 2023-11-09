import React from "react";
import { Link } from "react-router-dom";

const NoPage = () => {
  return (
    <div>
      <h1>404</h1>
      <p>Oops! The page you are looking for does not exist.</p>
      <Link to="/">Go back to home page</Link>
    </div>
  );
};

export default NoPage;
