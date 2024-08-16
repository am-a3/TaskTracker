//
//  ContentView.swift
//  TaskTracker
//
//  Created by Aleksandrs Maklakovs on 07/08/2024.
//

import SwiftUI

enum MenuView {
    case main_menu
    case tasks_menu
    case projects_menu
    case locations_menu
    case tags_menu
    case task_menu
}

struct Task: Hashable {
    var name: String
    var description: String
}

struct ContentView: View {
    @State private var ip_addr: String = ""
    @State private var username: String = ""
    @State private var password: String = ""
    @State private var current_view: MenuView = .main_menu
    @State private var is_connected: Bool = false
    
    var body: some View {
        NavigationView {
            VStack {
                HStack {
                    Text("IP:");
                    TextField(
                        "Server IP address",
                        text: $ip_addr
                    )
                    .textInputAutocapitalization(.never)
                    .disableAutocorrection(true)
                    .border(.secondary)
                };
                HStack {
                    Text("Usename:");
                    TextField(
                        "User name",
                        text: $username
                    )
                    .textInputAutocapitalization(.never)
                    .disableAutocorrection(true)
                    .border(.secondary)
                };
                HStack {
                    Text("Password:");
                    SecureField(
                        "Password",
                        text: $password
                    )
                    .textInputAutocapitalization(.never)
                    .disableAutocorrection(true)
                    .border(.secondary)
                };
                Button(is_connected ? "DISCONNECT" : "CONNECT"){
                    //Temporary for testing only:
                    if is_connected {
                        self.is_connected = false
                    }
                    else {
                        self.is_connected = true
                    }
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(is_connected ? .red : .green)
                Divider()
                NavigationLink(destination: TasksView()){
                    Text("TASKS")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                NavigationLink(destination: ProjectsView()){
                    Text("PROJECTS")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                NavigationLink(destination: LocationsView()){
                    Text("LOCATIONS")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                NavigationLink(destination: TagsView()){
                    Text("TAGS")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                Spacer()
            }
            .padding()
        }
    }
}

struct TaskView: View {
    @State  var task: Task
    @State private var is_done: Bool = false
    
    var body: some View {
        VStack {
            HStack {
                Spacer()
                Button("Delete"){
                    
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                .padding(.trailing, 8)
                .padding(.top, 5)
            }
            Divider()
            .frame(height: 2)
            .background(Color.blue)
            HStack{
                Text("Name: ")
                TextField(
                    task.name,
                    text: $task.name
                    )
                Spacer()
                Toggle(isOn: $is_done) {
                    Text("Done")
                }
                .toggleStyle(iOSCheckboxToggleStyle())
                .padding(.trailing, 8)
            }
            HStack {
                Text("Description: ")
                TextField(
                    task.description,
                    text: $task.description
                    )
                Spacer()
            }
            HStack {
                Text("Project:")
                //TODO: Drop down here
                Spacer()
            }
            HStack {
                Text("Location:")
                //TODO: Drop down here
                Spacer()
            }
            HStack {
                Text("Tags:")
                //TODO: Text input here
                Spacer()
            }
            Spacer()
        }
    }
}

struct iOSCheckboxToggleStyle: ToggleStyle {
    func makeBody(configuration: Configuration) -> some View {
        // 1
        Button(action: {

            // 2
            configuration.isOn.toggle()

        }, label: {
            HStack {
                // 3
                Image(systemName: configuration.isOn ? "checkmark.square" : "square")

                configuration.label
            }
        })
    }
}

struct TasksView: View {
    @State private var is_done: Bool = false
    private let test_task: [Task] = [Task(name: "Task 1", description: ""), Task(name: "Task 2", description: ""), Task(name: "Task 3", description: ""), Task(name: "Task 4", description: "")]
    private
    let test: Task = Task(name: "New task", description: "")
    
    var body: some View {
        VStack {
            HStack {
                Spacer()
                NavigationLink(destination: TaskView(task: test)){
                    Text("Create new")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                .padding(.trailing, 8)
                .padding(.top, 5)
            }
            Divider()
            .frame(height: 2)
            .background(Color.blue)
            ForEach(test_task, id: \.self) { value in
                HStack {
                    NavigationLink(destination: TaskView(task: value)){
                        Text(value.name)
                    }
                    .padding(.leading, 8)
                    Spacer()
                    Button(role: .destructive, action: {}) {
                        Label("", systemImage: "trash")
                    }
                    Toggle(isOn: $is_done) {
                        Text("Done")
                    }
                    .toggleStyle(iOSCheckboxToggleStyle())
                    .padding(.trailing, 8)
                }
                .padding(.top, 5)
                .padding(.bottom, 5)
                Divider()
            }
            Spacer()
        }
    }
}

struct ProjectsView: View {
    private let test_projects: [String] = ["Project 1", "Project 2", "Project 3", "Project 4"]
    
    var body: some View {
        VStack {
            HStack {
                Spacer()
                NavigationLink(destination: TasksView()){
                    Text("Create new")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                .padding(.trailing, 8)
                .padding(.top, 5)
            }
            Divider()
            .frame(height: 2)
            .background(Color.blue)
            ForEach(test_projects, id: \.self) { value in
                HStack {
                    Text(value)
                    .padding(.leading, 8)
                    Spacer()
                    Button(role: .destructive, action: {}) {
                        Label("", systemImage: "trash")
                    }
                }
                .padding(.top, 5)
                .padding(.bottom, 5)
                Divider()
            }
            Spacer()
        }
    }
}

struct LocationsView: View {
    private let test_locations: [String] = ["Location 1", "Location 2", "Location 3", "Location 4"]
    
    var body: some View {
        VStack {
            HStack {
                Spacer()
                NavigationLink(destination: TasksView()){
                    Text("Create new")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                .padding(.trailing, 8)
                .padding(.top, 5)
            }
            Divider()
            .frame(height: 2)
            .background(Color.blue)
            ForEach(test_locations, id: \.self) { value in
                HStack {
                    Text(value)
                    .padding(.leading, 8)
                    Spacer()
                    Button(role: .destructive, action: {}) {
                        Label("", systemImage: "trash")
                    }
                }
                .padding(.top, 5)
                .padding(.bottom, 5)
                Divider()
            }
            Spacer()
        }
    }
}

struct TagsView: View {
    private let test_tags: [String] = ["Tag 1", "Tag 2", "Tag 3", "Tag 4"]
    
    var body: some View {
        VStack {
            HStack {
                Spacer()
                NavigationLink(destination: TasksView()){
                    Text("Create new")
                }
                .buttonStyle(.bordered)
                .foregroundColor(.white)
                .background(.blue)
                .padding(.trailing, 8)
                .padding(.top, 5)
            }
            Divider()
            .frame(height: 2)
            .background(Color.blue)
            ForEach(test_tags, id: \.self) { value in
                HStack {
                    Text(value)
                    .padding(.leading, 8)
                    Spacer()
                    Button(role: .destructive, action: {}) {
                        Label("", systemImage: "trash")
                    }
                }
                .padding(.top, 5)
                .padding(.bottom, 5)
                Divider()
            }
            Spacer()
        }
    }
}

#Preview {
    ContentView()
}
