/**
 * Created by thatinstant on 5/21/17.
 */
var myDashboard = new Dashboard();
myDashboard.addWidget('TasksWidget', 'Number', {
    getData: function () {
        var self = this;
        Dashing.utils.get('tasks_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    interval: 3000
});