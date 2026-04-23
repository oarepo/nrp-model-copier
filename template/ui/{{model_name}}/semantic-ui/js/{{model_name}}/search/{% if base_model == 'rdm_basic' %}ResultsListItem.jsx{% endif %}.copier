import React from "react";
import PropTypes from "prop-types";
import _get from "lodash/get";

import { Item, Label } from "semantic-ui-react";
import { i18next } from "@translations/i18next";
import { SearchItemCreators } from "@js/invenio_app_rdm/utils";

export const ResultsListItem = ({ result }) => {
  const accessRights = _get(result, "ui.access_status", null);
  const createdDate = _get(
    result,
    "ui.created_date_l10n_short",
    "No creation date found."
  );
  const creators = _get(result, "ui.creators.creators", []);

  const publicationDate = _get(
    result,
    "ui.publication_date_l10n_long",
    i18next.t("No publication date found.")
  );
  const resourceType = _get(
    result,
    "ui.resource_type.title_l10n",
    i18next.t("No resource type")
  );
  const title = _get(result, "metadata.title", i18next.t("No title"));

  const viewLink = result.links.self_html;

  return (
    <Item key={result.id} data-testid="result-item">
      <Item.Content>
        <Item.Extra className="labels-actions">
          <Label horizontal size="small" className="primary theme-primary">
            {publicationDate}
          </Label>
          <Label horizontal size="small" className="neutral">
            {resourceType}
          </Label>
          {accessRights && accessRights.id !== "open" && (
            <Label title={`${accessRights.description_l10n}`}>
              {accessRights.title_l10n}
            </Label>
          )}
        </Item.Extra>
        <Item.Header as="h2">
          <a href={viewLink}>{title}</a>
        </Item.Header>
        <Item className="creatibutors">
          <SearchItemCreators creators={creators} othersLink={viewLink} />
        </Item>

        <Item.Extra>
          <small>
            <p>
              {createdDate && (
                <>
                  {i18next.t("Uploaded on")} <span>{createdDate}</span>
                </>
              )}
            </p>
          </small>
        </Item.Extra>
      </Item.Content>
    </Item>
  );
};

ResultsListItem.propTypes = {
  result: PropTypes.object.isRequired,
};

export default ResultsListItem;
