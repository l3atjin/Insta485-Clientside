import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';
import Form from './form'

class Comments extends React.Component {
  /* Display number of likes and like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { comments: "", newComment: "", car: [] };
    this.handleCommentChange = this.handleCommentChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
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
          comments: data.comments,
        });
      })
      .catch((error) => console.log(error));
  }
  handleCommentChange(input) {
    this.setState({newComment: input});
  }

  handleSubmit(input) {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: this.state.newComment })
    };
    fetch(this.props.url, requestOptions)
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.state.comments.push(data);
        this.setState({
          comments: this.state.comments,
        });
      })

  }

  render() {
    // This line automatically assigns this.state.numLikes to the const variable numLikes
    const {comments} = this.state;
    // console.log(comments);
    const items = [];
    var user_link = "/u/";
    // Loop Through Comments
    for(const comment of comments){
      user_link = "/u/" + comment["owner"];
      items.push(<div key={comment["commentid"]}>
                  <a href={user_link} >{comment["owner"]}</a>
                  <p>{comment["text"]}</p>
                 </div>
                );
    }

    // <Comments url={`${url}comments/`} /
    return (
      <div className="comments">
        {items}
        <div><Form textContent = {this.state.newComment} onCommentChange = {this.handleCommentChange} onSubmitChange = {this.handleSubmit}/></div>
      </div>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Comments;