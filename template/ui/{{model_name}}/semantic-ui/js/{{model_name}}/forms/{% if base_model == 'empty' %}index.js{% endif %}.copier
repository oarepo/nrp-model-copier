import { DepositFormApp, parseFormAppConfig, ExampleSection } from "@js/oarepo_ui/forms";
import { EmptyDepositRecordSerializer } from "@js/oarepo_ui/api";
import React from "react";
import ReactDOM from "react-dom";
import { SaveButton } from "@js/invenio_rdm_records";
import { Grid } from "semantic-ui-react";
const { rootEl, config, ...rest } = parseFormAppConfig();
const recordSerializer = new EmptyDepositRecordSerializer();

const componentOverrides = {
  [`${config.overridableIdPrefix}.TabForm.actions`]: () => (
    <Grid.Row data-testid="tab-form-actions-row">
      <div className="flex justify-end form-actions-row">
        <div>
          <SaveButton />
        </div>
      </div>
    </Grid.Row>
  ),
};

const sections = [ExampleSection];

ReactDOM.render(
  <DepositFormApp
    config={config}
    {...rest}
    sections={sections}
    recordSerializer={recordSerializer}
    componentOverrides={componentOverrides}
    useWizardForm
  />,
  rootEl,
);
