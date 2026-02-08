/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';

export class EstimationListController extends ListController {
   setup() {
       super.setup();
   }
   ImportRecords() {
       this.actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'import.estimation.wizard',
          name:'Import Estimation',
          view_mode: 'form',
          view_type: 'form',
          views: [[false, 'form']],
          target: 'new',
          res_id: false,
       });
   }
}

registry.category("views").add("button_in_tree", {
   ...listView,
   Controller: EstimationListController,
   buttonTemplate: "ama_zeroglare_crm.ListButtons",
});
