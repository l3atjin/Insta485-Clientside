import React from 'react';
import PropTypes from 'prop-types';
import Post from './post';
import Comments from './comments';


class Form extends React.Component {
    constructor(props) {
      super(props);
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event) {
      this.props.onCommentChange(event.target.value);
    }
  
    handleSubmit(event) {
      this.props.onSubmitChange();
      event.preventDefault();
    }
  
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
            <input type="text" value={this.props.textContent} onChange={this.handleChange} />
            <input type="submit" value="Submit" />
        </form>
      );
    }
  }

  /* Form.propTypes = {
    textContent: PropTypes.string.isRequired,
    onCommentChange: PropTypes.string.isRequired,
  }; */
  
  export default Form;
  