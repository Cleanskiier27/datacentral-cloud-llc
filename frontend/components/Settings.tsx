import React from 'react';
import { Shield, Users, Globe, Trash2 } from 'lucide-react';

export default function Settings() {
  return (
    <div className="max-w-4xl mx-auto p-6 md:p-8 space-y-8">
      <header>
        <h1 className="text-2xl font-normal text-gray-800 tracking-tight">Settings</h1>
        <p className="text-sm text-gray-500 mt-1">Property settings for example.com</p>
      </header>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-gray-100 flex items-start space-x-4">
          <div className="p-2 bg-green-50 rounded-lg">
            <Shield className="w-6 h-6 text-green-600" />
          </div>
          <div className="flex-1">
            <h2 className="text-lg font-medium text-gray-900">Ownership verification</h2>
            <p className="text-sm text-gray-500 mt-1">You are a verified owner</p>
          </div>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            Verified
          </span>
        </div>
        
        <div className="p-6 border-b border-gray-100 flex items-start space-x-4">
          <div className="p-2 bg-blue-50 rounded-lg">
            <Users className="w-6 h-6 text-blue-600" />
          </div>
          <div className="flex-1">
            <h2 className="text-lg font-medium text-gray-900">Users and permissions</h2>
            <p className="text-sm text-gray-500 mt-1">Manage who has access to this property</p>
          </div>
          <button className="text-sm font-medium text-blue-600 hover:text-blue-800">
            Manage
          </button>
        </div>

        <div className="p-6 border-b border-gray-100 flex items-start space-x-4">
          <div className="p-2 bg-purple-50 rounded-lg">
            <Globe className="w-6 h-6 text-purple-600" />
          </div>
          <div className="flex-1">
            <h2 className="text-lg font-medium text-gray-900">Change of address</h2>
            <p className="text-sm text-gray-500 mt-1">Tell Google when your site moves to a new domain</p>
          </div>
          <button className="text-sm font-medium text-blue-600 hover:text-blue-800">
            Start
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-red-200 shadow-sm overflow-hidden">
        <div className="p-6 flex items-start space-x-4">
          <div className="p-2 bg-red-50 rounded-lg">
            <Trash2 className="w-6 h-6 text-red-600" />
          </div>
          <div className="flex-1">
            <h2 className="text-lg font-medium text-gray-900">Remove property</h2>
            <p className="text-sm text-gray-500 mt-1">Remove this property from your Search Console account</p>
          </div>
          <button className="px-4 py-2 bg-red-50 hover:bg-red-100 text-red-700 text-sm font-medium rounded-lg transition-colors border border-red-200">
            Remove
          </button>
        </div>
      </div>
    </div>
  );
}
