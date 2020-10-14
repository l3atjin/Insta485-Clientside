import React from 'react';
import ReactDOM from 'react-dom';
import Likes from './likes';
import Feed from './feed';
import Post from './post';
import Comments from './comments';

// This method is only called once
ReactDOM.render(
  // Insert the likes component into the DOM
  <Feed url="/api/v1/p/" />,
  document.getElementById('reactEntry'),
);