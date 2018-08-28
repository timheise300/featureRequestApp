function featureRequest(data) {
    this.id = ko.observable(data.id);
    this.title = ko.observable(data.title);
    this.description = ko.observable(data.description);
    this.clientName = ko.observable(data.clientName);
    this.priority = ko.observable(data.priority);
    this.targetDate = ko.observable(data.targetDate);
    this.productArea = ko.observable(data.productArea);
}

function client(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.featureRequests = ko.observableArray(data.featureRequests);
}

function featureRequestListVM() {
    var self = this;
    self.clients = ko.observableArray();
    self.productAreasList = ko.observableArray([]);
    self.newFeatureRequest = ko.observable(new featureRequest());
    self.selectedClient = kko.observable();

    $.getJSON('/api/getClientData', function(clients) {
        var t = $.map(clients.tasks, function(item) {
            return new Task(item);
        });
        self.clients(t);
    });

    self.save = function() {
        return $.ajax({
            url: '/api/newRequest',
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(self.NewFeatureRequest),
            success: function(data) {
                console.log("Pushing to tasks array");
                self.selectedClient.featureRequests.push(new featureRequest(self.newFeatureRequest));
                return;
            },
            error: function() {
            return console.log("Failed to add new Feature Request");
            }
        });
    };
}

ko.applyBindings(new featureRequestListVM());