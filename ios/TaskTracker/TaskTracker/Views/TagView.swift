//
//  TagsView.swift
//  TaskTracker
//
//  Created by Aleksandrs Maklakovs on 21/08/2024.
//

import SwiftUI

struct TagView: View {
    
    var body: some View {
        VStack {
            Text("Hello!")
        }
    }
}

struct TagsView: View {
    private let test_tags: [String] = ["Tag 1", "Tag 2", "Tag 3", "Tag 4"]
    
    var body: some View {
        VStack {
            HStack {
                Spacer()
                NavigationLink(destination: TagView()){
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
