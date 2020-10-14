import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes and like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.submitLike = this.submitLike.bind(this);
    this.state = { numLikes: 5, logname_likes_this: 0 };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    // Call REST API to get number of likes
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          numLikes: data.likes_count,
          logname_likes_this: data.logname_likes_this,
        });
      })
      .catch((error) => console.log(error));
  }

  submitLike(){
    //Unlike
    if (this.state.logname_likes_this == 1){
        const requestOptions = {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
        };
        fetch(this.props.url, requestOptions)
          .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return
          })
          .then((data) => {
            this.setState({
              numLikes: this.state.numLikes - 1,
              logname_likes_this: 0,
            });
          })
        
    }
    //Like
    else {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // body: JSON.stringify({ text: "" })
     };
      fetch(this.props.url, requestOptions)
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return
        })
        .then((data) => {
          this.setState({
            numLikes: this.state.numLikes + 1,
            logname_likes_this: 1,
          });
        })
    }
    return;
  }

  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes
    // const { numLikes } = this.state;
    const {numLikes} = this.state.numLikes;
    // Render number of likes
    return (
      <div className="likes">
        <p>
          {this.state.numLikes}
          {' '}
          like
          {this.state.numLikes !== 1 ? 's' : ''}
        </p>
        <div>
          <button className="like-unlike-button" onClick={this.submitLike}>
              {this.state.logname_likes_this ? "Unlike" : "Like"}
          </button>
        </div>
      </div>
    );
  }
}

Likes.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Likes;