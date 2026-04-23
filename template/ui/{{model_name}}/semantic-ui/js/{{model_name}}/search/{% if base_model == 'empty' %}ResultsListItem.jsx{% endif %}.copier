import React from "react";
import PropTypes from "prop-types";
import { Item } from "semantic-ui-react";

export const ResultsListItem = ({ result }) => {
  const viewLink = result.links.self_html;
  return (
    <Item key={result.id} data-testid="result-item">
      <Item.Content>
        <Item.Header as="h2">
          <a href={viewLink}>{result.id}</a>
        </Item.Header>
      </Item.Content>
    </Item>
  );
};

ResultsListItem.propTypes = {
  result: PropTypes.object.isRequired,
};

export default ResultsListItem;
