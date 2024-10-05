//
//  ApiService.swift
//  TaskTracker
//
//  Created by Aleksandrs Maklakovs on 17/08/2024.
//

import Foundation

enum ApiError: Error {
    case runtimeError(String)
}

class ApiService {
    
    func requestTasks(server_url: String) async throws -> [TaskBasic] {
        var tasks: [TaskBasic]
        do {
            let url = URL(string: "\(server_url)/v1/tasks")!
            let (data, _) = try await URLSession.shared.data(from: url)
            tasks = try JSONDecoder().decode([TaskBasic].self, from: data)
        } catch {
            throw ApiError.runtimeError("Error")
        }
        
        return tasks
    }
    
    func requestTask(server_url: String, task_id: String) async throws -> Task {
        var task: Task
        do {
            let url = URL(string: "\(server_url)/v1/tasks/\(task_id)")!
            let (data, _) = try await URLSession.shared.data(from: url)
            task = try JSONDecoder().decode(Task.self, from: data)
        } catch {
            throw ApiError.runtimeError("Error")
        }
        
        return task
    }
    
    func requestDoneTasks(server_url: String) async throws -> [TaskBasic] {
        var tasks: [TaskBasic]
        do {
            let url = URL(string: "\(server_url)/v1/tasks/done")!
            let (data, _) = try await URLSession.shared.data(from: url)
            tasks = try JSONDecoder().decode([TaskBasic].self, from: data)
        } catch {
            throw ApiError.runtimeError("Error")
        }
        
        return tasks
    }
    
    func requestProjects(server_url: String) async throws -> [ProjectBasic] {
        var projects: [ProjectBasic]
        do {
            let url = URL(string: "\(server_url)/v1/projects")!
            let (data, _) = try await URLSession.shared.data(from: url)
            projects = try JSONDecoder().decode([ProjectBasic].self, from: data)
        } catch {
            throw ApiError.runtimeError("Error")
        }
        
        return projects
    }
    
    func requestProject(server_url: String, project_id: String) async throws -> Project {
        var project: Project
        do {
            let url = URL(string: "\(server_url)/v1/projects/\(project_id)")!
            let (data, _) = try await URLSession.shared.data(from: url)
            project = try JSONDecoder().decode(Project.self, from: data)
        } catch {
            throw ApiError.runtimeError("Error")
        }
        
        return project
    }
    
    func requestLocations(server_url: String) async throws -> [LocationBasic] {
        var locations: [LocationBasic]
        do {
            let url = URL(string: "\(server_url)/v1/locations")!
            let (data, _) = try await URLSession.shared.data(from: url)
            locations = try JSONDecoder().decode([LocationBasic].self, from: data)
        } catch {
            throw ApiError.runtimeError("Error")
        }
        
        return locations
    }
    
    func requestLocation(server_url: String, location_id: String) async throws -> Location {
        var location: Location
        do {
            let url = URL(string: "\(server_url)/v1/locations/\(location_id)")!
            let (data, _) = try await URLSession.shared.data(from: url)
            location = try JSONDecoder().decode(Location.self, from: data)
        } catch {
            throw ApiError.runtimeError("Error")
        }
        
        return location
    }
    
    func requestTags(server_url: String) async throws -> [TagBasic] {
        var tag: [TagBasic]
        do {
            let url = URL(string: "\(server_url)/v1/tags")!
            let (data, _) = try await URLSession.shared.data(from: url)
            tag = try JSONDecoder().decode([TagBasic].self, from: data)
        } catch {
            throw ApiError.runtimeError("Error")
        }
        
        return tag
    }
    
    func requestTag(server_url: String, tag_id: String) async throws -> Tag {
        var tag: Tag
        do {
            let url = URL(string: "\(server_url)/v1/tags/\(tag_id)")!
            let (data, _) = try await URLSession.shared.data(from: url)
            tag = try JSONDecoder().decode(Tag.self, from: data)
        } catch {
            throw ApiError.runtimeError("Error")
        }
        
        return tag
    }
}
