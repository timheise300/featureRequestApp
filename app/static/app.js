function FeatureRequest(data) {
    if (data) {
        this.id = ko.observable(data.id);
        this.title = ko.observable(data.title);
        this.description = ko.observable(data.description);
        this.client_id = ko.observable(data.client_id);
        this.client_priority = ko.observable(data.client_priority);
        this.target_date = ko.observable(data.target_date);
        this.product_area = ko.observable(data.product_area);
    } else {
        this.id = ko.observable();
        this.title = ko.observable();
        this.description = ko.observable();
        this.client_id = ko.observable();
        this.client_priority = ko.observable();
        this.target_date = ko.observable();
        this.product_area = ko.observable();
    }
}

function Client(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.feature_requests = ko.observableArray();
    
    var requestArray = ko.utils.arrayMap(data.feature_requests, function(feature_request) {
        return new FeatureRequest(feature_request);
    });

    for (var i = 0; i < requestArray.length; i++) {
        this.feature_requests.push(requestArray[i]);
    }

    this.feature_requests.sort(function (left, right) { 
        return left.client_priority == right.client_priority ? 0 : (left.client_priority < right.client_priority ? 1 : -1)
    });
}

function featureRequestListVM() {
    var self = this;
    self.clients = ko.observableArray();
    self.product_areas_list = ko.observableArray([]);
    self.new_feature_request = ko.observable(new FeatureRequest());
    self.errors = ko.observableArray();
    self.selected_client = ko.observable();
    self.form_priority_max = ko.observable();
    self.product_areas = ko.observableArray([
        { "id": "Claims", "title": "Claims" },
        { "id": "Policies", "title": "Policies" },
        { "id": "Billing", "title": "Billing" },
        { "id": "Reports", "title": "Reports" },
    ]);

    $.getJSON("/api/clients/", function(data) {
        var mappedClients = $.map(data['clients'], function(item) { return new Client(item) });
        self.clients(mappedClients);
        self.selected_client(new Client(self.clients()[0]));
        self.form_priority_max(self.selected_client().feature_requests().length + 1);
    });

    self.saveRequest = function(form_element) {
        var data = $('#newFeatureRequest').serializeArray().map(function(x){this[x.name] = x.value; return this;}.bind({}))[0];

        if(data.id) {
            self.updateRequest(form_element);
        } else {
            self.addRequest(data);
        }
    }

    self.updateSelectedClient = function(selectedClient) {
        self.selected_client(new Client(selectedClient));
    }

    self.addRequest = function(data) {
        console.log(data);
        $.ajax(
            '/api/feature_requests/add/',
            {
                contentType: 'application/json;',
                method: 'POST',
                data: JSON.stringify(data),
                success: function (data) {
                    $('#requestForm').modal('hide');
                    self.selected_client().feature_requests.push(new FeatureRequest(ko.toJS(data['data'][0])));
                    self.selected_client().feature_requests.sort(function (left, right) { 
                        return left.client_priority == right.client_priority ? 0 : (left.client_priority < right.client_priority ? 1 : -1)
                    });
                },
                error: function (errors) {
                    console.log(errors);
                    self.errors(errors.responseJSON.errors);
                }
            }
        );
    };
    
    self.initRequestForm = function(feature_request) {
        self.new_feature_request(new FeatureRequest(ko.toJS(feature_request)));
        self.new_feature_request().client_id.subscribe(function(newValue) {
            var selectedClient = ko.utils.arrayFirst(self.clients(), function (item) {
                return item.id() == newValue;
            });
            self.form_priority_max(selectedClient.feature_requests().length + 1);
        });
        $('#requestForm').modal('show');
    }

    self.updateRequest = function(form_element){
        var data = $('#newFeatureRequest').serializeArray().map(function(x){this[x.name] = x.value; return this;}.bind({}))[0];

        $.ajax(
            '/api/feature_requests/' + data.id + '/',
            {
                contentType: 'application/json;',
                method: 'POST',
                data: JSON.stringify(data),
                success: function (new_data) {
                    $('#requestForm').modal('hide');
                    var oldLocation = ko.utils.arrayFirst(self.selected_client().feature_requests, function (item) {
                        return ko.utils.unwrapObservable(item.id()) == data.id;
                    });
                    self.selected_client().feature_requests.replace(oldLocation, new FeatureRequest(ko.toJS(new_data['data'][0])));
                    self.selected_client().feature_requests.sort(function (left, right) { 
                        return left.client_priority == right.client_priority ? 0 : (left.client_priority < right.client_priority ? 1 : -1)
                    });
                },
                error: function (errors) {
                    console.log(errors);
                    self.errors(errors.responseJSON.errors);
                }
            }
        );
    };
}

ko.applyBindings(new featureRequestListVM());