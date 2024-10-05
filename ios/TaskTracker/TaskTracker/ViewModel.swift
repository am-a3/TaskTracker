//
//  ViewModel.swift
//  TaskTracker
//
//  Created by Aleksandrs Maklakovs on 18/08/2024.
//

import Foundation

class ViewModel: ObservableObject {
    @Published var ip_addr: String = ""
    @Published var username: String = ""
    @Published var password: String = ""
    @Published var tasks_overview: [TaskBasic] = []
    @Published var tasks_done_overview: [TaskBasic] = []
    @Published var current_task: Task = Task()
    @Published var projects_overview: [ProjectBasic] = []
    @Published var current_project: Project = Project()
    private var api_service = ApiService()
    
    func requestTasks() async {
        do {
            self.tasks_overview = try await api_service.requestTasks(server_url: ip_addr)
        }
        catch {
            self.tasks_overview = [TaskBasic(name:"DummyTask")]
        }
    }
    
    func requestDoneTasks() async {
        do {
            self.tasks_done_overview = try await api_service.requestTasks(server_url: ip_addr)
        }
        catch {
            self.tasks_done_overview = [TaskBasic(name:"DummyTask")]
        }
    }
    
    func requestTask(uuid: String) async throws {
        self.current_task = try await api_service.requestTask(server_url: ip_addr, task_id: uuid)
    }
    
    func requestProjects() async throws {
        self.projects_overview = try await api_service.requestProjects(server_url: ip_addr)
    }
    
    func requestProject(uuid: String) async throws {
        self.current_project = try await api_service.requestProject(server_url: ip_addr, project_id: uuid)
    }
}
