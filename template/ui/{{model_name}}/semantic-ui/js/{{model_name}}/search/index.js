import {
  parseSearchAppConfigs,
  createSearchAppsInit,
} from "@js/oarepo_ui/search";
import ResultsListItem from "./ResultsListItem";

/** NOTE: This reads configs for any search app present on a page.
 *   In HTML/Jinja, a single search app instance is typically represented
 *   by a DOM element carrying the search app config. To customize components
 *   in a specific search app instance, you need to obtain its
 *   `overridableIdPrefix` from the corresponding config first.
 */
const [{ overridableIdPrefix }] = parseSearchAppConfigs();

export const componentOverrides = {
  /** NOTE: You can then replace any existing search ui
   * component with your own implementation, e.g.:
   */
  [`${overridableIdPrefix}.ResultsList.item`]: ResultsListItem,
};

createSearchAppsInit({ componentOverrides });
