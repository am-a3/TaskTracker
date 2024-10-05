//
//  DataModelsLocal.swift
//  TaskTracker
//
//  Created by Aleksandrs Maklakovs on 29/08/2024.
//

import Foundation
import SwiftData

@Model final class TaskLocal {
    @Attribute(.unique) let id = UUID()
    var name: String
    var task_description: String
    var project: ProjectLocal?
    var location: [LocationLocal]
    var is_done: Bool
    var tags: [TagLocal]
    
    init(name: String, task_description: String, project: ProjectLocal?, location: [LocationLocal],
         is_done: Bool, tags: [TagLocal]) {
        self.name = name
        self.task_description = task_description
        self.project = project
        self.location = location
        self.is_done = is_done
        self.tags = tags
    }
    
    init(name: String) {
        self.name = name
        self.task_description = ""
        self.location = []
        self.is_done = false
        self.tags = []
    }
    
    init() {
        self.name = ""
        self.task_description = ""
        self.location = []
        self.is_done = false
        self.tags = []
    }
}

@Model final class ProjectLocal {
    @Attribute(.unique) let id = UUID()
    var name: String
    var project_description: String
    var tasks: [TaskLocal]
    
    init(name: String, project_description: String, tasks: [TaskLocal]) {
        self.name = name
        self.project_description = project_description
        self.tasks = tasks
    }
    init(name: String) {
        self.name = name
        self.project_description = ""
        self.tasks = []
    }
}

@Model final class LocationLocal {
    @Attribute(.unique) let id = UUID()
    var name: String
    var location_description: String
    
    init(name: String, location_description: String) {
        self.name = name
        self.location_description = location_description
    }
}

@Model final class TagLocal {
    @Attribute(.unique) let id = UUID()
    var name: String
    var tag_description: String
    
    init(name: String, tag_description: String) {
        self.name = name
        self.tag_description = tag_description
    }
}
