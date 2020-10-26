import React from 'react';
import PropTypes from 'prop-types';

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
    const { textContent } = this.props
    return (
      <form className = "comment-form" onSubmit={this.handleSubmit}>
        <input type="text" value={this.props.textContent} onChange={this.handleChange} />
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

Form.propTypes = {
  textContent: PropTypes.string.isRequired,
  onCommentChange: PropTypes.func.isRequired,
  onSubmitChange: PropTypes.func.isRequired,
};

export default Form;
