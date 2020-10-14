import React from 'react';
import PropTypes from 'prop-types';
import Feed from './feed';
import Likes from './likes';
import Comments from './comments';
import moment from "moment";

class Post extends React.Component {
  /* Display number of likes and like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    // Do we declare Likes() and Comments() here ?
    this.state = { owner: "junk", post_url: "junk", created: "junk",
                    image_url: "junk", owner_img_url: "junk",
                    post_show_url: "junk", owner_show_url: "junk"};
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    // Call REST API to get 10 posts
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      // Data
      .then((data) => {
        // Grab Post Data
        this.setState({
          owner: data.owner,
          show_post_url: data.show_post_url,
          post_url: data.url,
          created: data.age,
          owner_img_url: data.owner_img_url,
          image_url: data.img_url,
          owner_show_url : data.owner_show_url,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes

    // Render Post
    var purl = "";
    purl = this.state.post_url + "likes/";
    return (
      <div className="post">
        <p> {this.state.owner} </p>
        <img src = {this.state.owner_img_url} alt="owner_img"/>
        <img src= {this.state.image_url} alt ="post_img"/>
		    <a href = {this.state.owner_show_url} > {this.state.owner} </a>
		    <a href = {this.state.post_url}> {moment.utc(this.state.created).fromNow()}</a>
        <Comments url={this.props.url + "comments/"}/>
        <Likes url={this.props.url + "likes/"}/>
      </div>
    );
      

    return result;
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;