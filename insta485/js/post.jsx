import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';
import Likes from './likes';
import Comments from './comments';

class Post extends React.Component {
  /* Display number of likes and like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    // Do we declare Likes() and Comments() here ?
    this.state = {
      owner: '',
      post_url: '',
      created: '',
      image_url: '',
      owner_img_url: '',
      owner_show_url: '',
      didLikeImg: false,
      post_show_url: ''
    };

    this.handleDoubleClick = this.handleDoubleClick.bind(this);
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
          post_url: data.url,
          created: data.age,
          owner_img_url: data.owner_img_url,
          image_url: data.img_url,
          owner_show_url: data.owner_show_url,
          post_show_url: data.post_show_url
        });
      })
      .catch((error) => console.log(error));
  }

  handleDoubleClick() {
    this.setState({
      didLikeImg: true,
    });
  }

  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes

    // Render Post
    return (
      <div className="post">
    
        <a href={this.state.owner_show_url}><img src={this.state.owner_img_url} alt="owner_img" /></a>
        <img src={this.state.image_url} alt="post_img" onDoubleClick={this.handleDoubleClick} />
        <a href={this.state.owner_show_url} >
          {' '}
          {this.state.owner }
          {' '}
        </a>
        <a href={this.state.post_show_url}>
          {' '}
          {moment.utc(this.state.created).fromNow() }
        </a>
        <Comments url={`${this.props.url}comments/`} />
        <Likes url={`${this.props.url}likes/`} didLike={this.state.didLikeImg} />
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;
