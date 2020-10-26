import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';

class Feed extends React.Component {
  /* Display number of likes and like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state= { postsJson: [] };
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
          postsJson: data.results,
          next: data.next,
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes

    // Render number of likes
    const items = [];

    for (const el of this.state.postsJson) {
      items.push(<Post url={el.url} key={el.url + "yus"}/>);
    }

    return (
      <div className="feed">
        <div>{items}</div>
      </div>
    );
  }
}

Feed.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Feed;
